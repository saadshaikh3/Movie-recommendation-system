screen_helper = '''
#:import CardTransition kivy.uix.screenmanager.CardTransition
#:import FallOutTransition kivy.uix.screenmanager.FallOutTransition
#:import NoTransition kivy.uix.screenmanager.NoTransition

ScreenManager:
    LogoScreen:
    MovieScreen:
    RecommendationScreen:

<LogoScreen>
    name :'logoscreen'
    Image:
        source: 'sskenterprise.jpg'
        size: self.texture_size


<MovieScreen>:
    name:'Movie'
    FloatLayout:
        orientation: 'horizontal'
        canvas:
            Rectangle:
                source: 'bgblue.jpg'
                size: self.size
                pos: self.pos



    MDLabel:
        text: "Welcome to the"
        halign:'center'
        font_size: "35px"
        color: rgba("#ffffff")
        # pos_hint: {'center_x': 0.6, 'center_y': 0.9}
        pos:(10,470)
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: "MOVIE MANIA"
        halign:'center'
        font_size: "45px"
        color: rgba("#ffffff")
        # pos_hint: {'center_x': 0.6, 'center_y': 0.9}
        pos:(10,420)
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: "can't decide what to watch? well\\ndont worry as we have got you covered."
        halign:'center'
        font_size: "35px"
        color: rgba("#ffffff")
        # pos_hint: {'center_x': 0.6, 'center_y': 0.9}
        pos:(10,340)
        size_hint_y: None
        height: self.texture_size[1]


    MDTextField:
        id: field

        dropdown_bg: app.theme_cls.bg_normal

        # pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        size_hint_x: None
        width: "200dp"
        hint_text: "Movie Names"
        pos:(100,280)
        on_focus: if self.focus: app.menu.open()
        normal_color : [255/255,255/255,255/255,1]
        color_active : [1,1,1,1]

    MDTextField:
        id: ratings
        dropdown_bg: app.theme_cls.bg_normal
        fill_color: 1,1,1,1
        size_hint_x: None
        width: "200dp"
        hint_text: "Rating"
        pos:(500,280)
        on_focus: if self.focus: app.rating_menu.open()
        normal_color : [255/255,255/255,255/255,1]
        color_active : [1,1,1,1]

    Button:
        text:'FIND'
        font_color: rgba("#000000")
        font_size:24
        # background_normal: ''
        background_color: rgba("#ffffff")
        size: 250, 50
        size_hint: None, None
        pos:(250,60)
        on_press:
            #root.manager.current = 'Recommendation'
            app.get_my_movies()


<RecommendationScreen>:
    name:'Recommendation'
    AnchorLayout:
        id:anchor_layout

    MDToolbar:
        title: 'Recommended Movies'
        type: 'top'
        pos_hint: {"top": 1}
        elevation:10

    MDBottomAppBar:
        MDToolbar:
            title:'SSK Enterprises'
            mode: 'end'
            type: 'bottom'
            on_action_button: 
                app.back()
                app.root.transition = NoTransition()
                root.manager.current = 'Movie'

            icon: 'language-python'

'''
