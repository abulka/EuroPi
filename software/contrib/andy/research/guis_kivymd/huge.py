from pprint import pprint , pformat
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import (
    RectangularRippleBehavior,
    BackgroundColorBehavior,
    RectangularElevationBehavior,
    CommonElevationBehavior,
    SpecificBackgroundColorBehavior,
)
from kivy.properties import StringProperty,ObjectProperty,ListProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.behaviors import DragBehavior
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Animation kivy.animation.Animation
#:import CommonElevationBehavior kivymd.uix.behaviors.CommonElevationBehavior

<DragLabel>:
    # Define the properties for the DragLabel
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    drag_distance: 0
    color:0,0,0,1

<Test_box@RectangularElevationBehavior+MDBoxLayout>:
    elevation: 20

<RectangularElevationButton>:
    size_hint: None, None
    size: "80dp", "50dp"
    # on_press:
    #     self.elevation = self.elevation + 5
    on_release:
        # self.elevation = self.elevation-5 if self.elevation > 4 else self.elevation
        # self.width = self.width + 10
        self.height = self.height + 10
    MDLabel:
        text:str(root.elevation)
        center:root.center

MDScreen:
    canvas.before:
        Color:
            rgba: get_color_from_hex("#e4e6e4")
        Rectangle:
            pos:self.pos
            size:self.size
    # on_touch_down: Animation(angle=45).start(card)
    MDBoxLayout:
        orientation:"vertical"
        ScrollView:
            StackLayout:
                size_hint_y:None
                height:self.minimum_height
                on_children:
                    self.height=self.minimum_height
                id:container_box
                padding: dp(80)
                spacing: dp(60)
                # cols: 9
                Test_box:
                    id:joycon
                    pos_hint: {"center":[0.5,0.2]}
                    md_bg_color:1,0,0,1
                    size_hint:None,None
                    size:50,50
                    DragLabel:
                        size_hint: None,None
                        size:self.parent.size
                        pos:self.parent.center
                        text: 'Drag me'
                        objeto: container_box
        MDRaisedButton:
            text: "Force light [20,10]"
            on_release:
                container_box.children[0].force_shadow_pos([20,10])
        MDSlider:
            size_hint_y:None
            height:dp(48)
            min: -90
            max: 90
            value: 0
            on_value:
                app.angle=self.value
        MDLabel:
            text:str(app.angle)
            size_hint_y:None
            height:dp(48)
'''

class DragLabel(DragBehavior, Label):
    objeto = ObjectProperty(None)
    origen = ListProperty(None)

    def on_touch_down(self, touch):
        x=super().on_touch_down(touch)
        self.origen=self.pos
        if touch.grab_current is self:
            pass
        return x

    def on_touch_move(self,touch):
        if self.objeto and self.origen:
            if not self.objeto.children:
                return
            self.objeto.children[1].force_shadow_pos([
                (self.origen[0]-self.pos[0])*.3,
                (self.origen[1]-self.pos[1])*.3,
            ])
        x = super().on_touch_move(touch)
        return x
    pass

    def on_touch_up(self,touch):
        x = super().on_touch_up(touch)
        if self.origen:
            self.pos = self.origen
        if self.objeto:
            self.objeto.children[1].force_shadow_pos([0,0])
        return x

class RectangularElevationButton(
        RectangularElevationBehavior,
        SpecificBackgroundColorBehavior,
        RectangularRippleBehavior,
        ButtonBehavior,
        BoxLayout,
    ):
    # md_bg_color = [1,.5,1,.91]
    # md_bg_color = ([1]*3 ) + [.2]
    md_bg_color = [1]*4
    text=StringProperty("")

class Test(MDApp):
    angle = NumericProperty(0)
    def build(self):
        x = Builder.load_string(KV)
        for i in range(10,48):
            x.ids.container_box.add_widget(
                RectangularElevationButton(
                    elevation=i,
                    angle = self.angle
                    # _hard_shadow_cl=[0,0,1,1],
                    # _soft_shadow_cl=[1,0,0,.45],
                )
            )
            # self.bind(angle=lambda z,y: setattr(x,"angle",y))
        return x
    def on_angle(self,*dt):
        for i in self.root.ids.container_box.children:
            i.angle = self.angle

Test().run()
