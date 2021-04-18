import pandas as pd
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import numpy as np
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from GUI import screen_helper

path_for_movies = 'movies.csv'
path_for_ratings = 'ratings.csv'

movies = pd.read_csv(path_for_movies)
movies.head()

ratings = pd.read_csv(path_for_ratings)
ratings.head()

# MERGING THE TWO DATASETS
ratings = pd.merge(movies, ratings)
ratings.head()

# DATA WRANGLING
ratings = ratings.drop(['genres', 'timestamp'], axis=1)
user_ratings = ratings.pivot_table(index=['userId'], columns=['title'], values='rating')
user_ratings.head()

# DROP ALL THE MOVIES THAT HAVE NOT BEEN RATED BY EVEN 10 USERS
user_ratings = user_ratings.dropna(thresh=10, axis=1).fillna(0)
guitext = user_ratings.columns
guitext.to_numpy()
guitext = np.random.choice(guitext, 200)

# NOW WE CHECK THE CORRELATION BETWEEN DIFFERENT MOVIES USING PEARSON CORRELATION
item_similarity_df = user_ratings.corr(method='pearson')
item_similarity_df.head()


# RECOMMENDER
# def get_similar_movies(movie_name, user_rating):
#     similar_score = item_similarity_df[movie_name] * (user_rating - 2.5)
#     similar_score = similar_score.sort_values(ascending=False).head(10)
#
#     similar_score = similar_score.to_frame()
#     #     similar_score = similar_score.to_frame()
#     return similar_score.index.to_numpy()
#

class LogoScreen(Screen):
    pass


class MovieScreen(Screen):
    pass


class RecommendationScreen(Screen):
    pass


sm = ScreenManager()
sm.add_widget(LogoScreen(name='logoscreen'))
sm.add_widget(MovieScreen(name='Movie'))
sm.add_widget(RecommendationScreen(name='Recommendation'))


def callbackfun(obj):
    MDApp.get_running_app().root.current = 'Movie'


class MovieRecommender(MDApp):
    def __init__(self):
        super().__init__()
        self.screen = Builder.load_string(screen_helper)
        self.theme_cls.primary_palette = 'Cyan'
        self.theme_cls.theme_style = "Light"
        Clock.schedule_once(self.for_movies)
        Clock.schedule_once(self.for_ratings)
        self.movie_name = ''
        self.user_ratings = ''

    def build(self):
        # loading_screen()
        Clock.schedule_once(callbackfun, 5)

        return self.screen

    def for_movies(self, *args):
        menu_items = [{"text": f"{i}"} for i in guitext]
        self.menu = MDDropdownMenu(
            caller=self.screen.get_screen('Movie').ids.field,
            items=menu_items,
            position="bottom",
            width_mult=4,
            callback=self.set_item
        )
        self.menu.bind(on_release=self.set_item)

    def set_item(self, instance):
        self.screen.get_screen('Movie').ids.field.text = instance.text
        self.movie_name = instance.text

    def for_ratings(self, *args):
        ratings_menu_items = [{"text": f"{i}"} for i in range(1, 6)]
        self.rating_menu = MDDropdownMenu(
            caller=self.screen.get_screen('Movie').ids.ratings,
            items=ratings_menu_items,
            position="bottom",
            width_mult=4,
            callback=self.set_ratings
        )
        self.menu.bind(on_release=self.set_ratings)

    def set_ratings(self, instance):
        self.screen.get_screen('Movie').ids.ratings.text = instance.text
        self.user_ratings = float(instance.text)

    def get_similar_movies(self, mn, ur):
        self.rlist = []
        self.rlist_final = []
        similar_score = item_similarity_df[mn] * (ur - 2.5)
        similar_score = similar_score.sort_values(ascending=False).head(11)

        similar_score = similar_score.to_frame()
        similar_score_m = similar_score.index.to_numpy()

        for i in similar_score_m:
            self.rlist.append(i)
        for i in range(1, len(self.rlist)):
            temp = [i, self.rlist[i]]
            self.rlist_final.append(temp)

        return self.rlist_final

    def get_my_movies(self):
        movieName = self.screen.get_screen('Movie').ids.field.text
        rating = self.screen.get_screen('Movie').ids.ratings.text
        if movieName.split() == [] or rating.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='Retry', on_release=self.close_username_dialog)
            self.dialog = MDDialog(title='Invalid Input', text='Please Enter a valid Input', size_hint=(0.7, 0.2),
                                   buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
            MDApp.get_running_app().root.current = 'Movie'
            return

        MDApp.get_running_app().root.current = 'Recommendation'
        cancel_btn_username_dialogue = MDFlatButton(text='Continue', on_release=self.close_username_dialog)
        self.dialog = MDDialog(title='Movies', text='These are the Top 10 Movies'
                                                    ' selected for you.', size_hint=(0.7, 0.2),
                               buttons=[cancel_btn_username_dialogue])
        self.dialog.open()
        MDApp.get_running_app().root.current = 'Recommendation'
        self.recommendation_given = self.get_similar_movies(self.movie_name, self.user_ratings)
        self.data_tables = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[("S.No", dp(30)), ("Titles", dp(100))],
            row_data=self.recommendation_given
        )

        self.screen.get_screen('Recommendation').ids.anchor_layout.add_widget(self.data_tables)

    def close_username_dialog(self, obj):
        self.dialog.dismiss()

    def back(self):
        self.screen.get_screen('Movie').ids.field.text = ''
        self.screen.get_screen('Movie').ids.ratings.text = ''


MovieRecommender().run()
