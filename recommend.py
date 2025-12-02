import pandas as pd
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender(QWidget):
    def __init__(self):
        super().__init__()
        self.set_ui()
        self.display_data()
        self.setObjectName("mywindow")

    def set_ui(self):
        self.setWindowTitle("Entertainment Hub")
        self.setWindowIcon(QIcon("images/icon.png"))
        self.setGeometry(200,300,500,600)

        #For layout
        v=QVBoxLayout()
        h=QHBoxLayout()

        #Creating widget
        self.lbl1=QLabel("Enter movie name: ")
        self.txt1=QLineEdit()
        self.txt1.setPlaceholderText("Movie name")
        self.btn=QPushButton("Recommend")
        self.btn.clicked.connect(self.recommend_me)
        self.result=QTextEdit()
        self.result.setReadOnly(True)

        #Adding widget and layout
        h.addWidget(self.lbl1)
        h.addWidget(self.txt1)
        v.addLayout(h)
        v.addWidget(self.btn)
        v.addWidget(self.result)

        #adding stylesheet
        self.setStyleSheet('''
        #mywindow{
        background-color:#302e2e;
        }
        
        QLabel{
        font-family:Times New Roman;
        font-size:16px;
        font-weight:bold;
        color:#f3e3df;
        }
        
        QLineEdit{
        font-family:Times New Roman;
        font-size:14px;
        padding:4px;
        background-color:#7a7878;
        color:#f3e3df;
        }
        
        QPushButton{
        padding:4px;
        font-family:Times New Roman;
        font-size:14px;
        background-color:#252222;
        color:#b32b0a;
        border:1px solid #b32b0a;
        border-radius:5px;
        width:120px;
        margin-top:5px;
        margin_bottom:8px;
        }
        
        QPushButton:hover{
         background-color:#0d0b0a;
         color:#f3461c;
         border:1px solid #f3461c;
         font-weight:bold;
        }
        
        QTextEdit{
        background-color:#7a7878;
        }
        ''')
        self.setLayout(v)

    #function for display data store in csv file
    def display_data(self):
        try:
            self.m=pd.read_csv("movie.csv")
            self.m['movie_genre']=self.m['movie_genre'].fillna("")
            self.vectorizer=TfidfVectorizer(stop_words='english')
            self.my_matrix=self.vectorizer.fit_transform(self.m["movie_genre"])
            self.similarity=cosine_similarity(self.my_matrix)

        except Exception as ex:
            #display message box if csv file is not loaded
            QMessageBox.warning(self,"Not Loaded",f"Failed to load\n\n{str(ex)}")
            sys.exit()

    #function for recommendation
    def recommend_me(self):
        user_movie=self.txt1.text().strip()

        #if user try to fill empty in movie name box
        if user_movie=="":
            QMessageBox.warning(self,"Empty",'Please enter a movie name for recommendation.')
            return

        #if typed movie is not in list
        if user_movie not in list(self.m['movie_title']):
            QMessageBox.warning(self,"Not found",'Movie not found.')
            return

        #For reading title and genre in csv
        ind=self.m[self.m['movie_title']==user_movie].index[0]
        my_genre=self.m.loc[ind,'movie_genre']
        idm_score=list(enumerate(self.similarity[ind]))
        sort_movie=sorted(idm_score,key=lambda x:x[1],reverse=True)
        recommend_data=[]

        #for each data in csv file
        for i,sc in sort_movie:
            genre=self.m.loc[i,'movie_genre']
            #If given movie's genre match with the genre stored in csv
            if my_genre in genre or genre in my_genre:
                #In recommendation it will avoid to show same movie name enter by user
                if self.m.loc[i,"movie_title"]!=user_movie:
                   t=self.m.iloc[i]['movie_title']
                   g=self.m.iloc[i]['movie_genre']
                   y=self.m.iloc[i]['years']
                   i_sc=self.m.iloc[i]['imb_rating']
                   show_detail=f"Title: {t} | Genre: {g} | Year: {y} | IMB Rating: {i_sc}"
                   recommend_data.append(show_detail)


        if recommend_data:
         self.result.setText("\n".join(recommend_data))

        else:
            self.result.setText("No movie with same genre is found.")


if __name__=="__main__":
    a=QApplication(sys.argv)
    w=MovieRecommender()
    w.show()
    sys.exit(a.exec_())
