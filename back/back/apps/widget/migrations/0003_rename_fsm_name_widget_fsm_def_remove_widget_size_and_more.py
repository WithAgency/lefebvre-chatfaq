# Generated by Django 4.1.13 on 2023-11-29 15:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("widget", "0002_rename_layout_widget_size_remove_theme_widget_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="widget",
            old_name="fsm_name",
            new_name="fsm_def",
        ),
        migrations.RemoveField(
            model_name="widget",
            name="size",
        ),
        migrations.AddField(
            model_name="widget",
            name="fullScreen",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="widget",
            name="manage_user_id",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="widget",
            name="maximized",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="theme",
            name="data",
            field=models.JSONField(
                default={
                    "chatfaq-color-alertMessage-text": {
                        "name": "alertMessage-text",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#e7e8e9", "light": "#545a64"},
                    },
                    "chatfaq-color-bubbleButton-background": {
                        "name": "bubbleButton-background",
                        "section": "colors",
                        "type": "gradient",
                        "value": "linear-gradient(135deg, #CE0578 0%, #463075 100%)",
                    },
                    "chatfaq-color-bubbleButton-background-hover": {
                        "name": "bubbleButton-background-hover",
                        "section": "colors",
                        "type": "gradient",
                        "value": "linear-gradient(135deg, #463075 0%, #220D44 100%)",
                    },
                    "chatfaq-color-chat-background": {
                        "name": "chat-background",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#4D4160", "light": "#dfdaea"},
                    },
                    "chatfaq-color-chatInput-background": {
                        "name": "chatInput-background",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#3c2d52", "light": "#cac2da"},
                    },
                    "chatfaq-color-chatInput-border": {
                        "name": "chatInput-border",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#1A0438", "light": "#9a8eb5"},
                    },
                    "chatfaq-color-chatInput-text": {
                        "name": "chatInput-text",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#FFFFFF", "light": "#020C1C"},
                    },
                    "chatfaq-color-chatMessageBot-background": {
                        "name": "chatMessageBot-background",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#3c2d52", "light": "#cac2da"},
                    },
                    "chatfaq-color-chatMessageBot-text": {
                        "name": "chatMessageBot-text",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#FFFFFF", "light": "#020C1C"},
                    },
                    "chatfaq-color-chatMessageHuman-background": {
                        "name": "chatMessageHuman-background",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#1A0438", "light": "#463075"},
                    },
                    "chatfaq-color-chatMessageHuman-text": {
                        "name": "chatMessageHuman-text",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#FFFFFF", "light": "#FFFFFF"},
                    },
                    "chatfaq-color-chatMessageReference-background": {
                        "name": "chatMessageReference-background",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#1A0438", "light": "rgba(70, 48, 117, .1)"},
                    },
                    "chatfaq-color-chatMessageReference-text": {
                        "name": "chatMessageReference-text",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#dfdaea", "light": "#463075"},
                    },
                    "chatfaq-color-chatMessageReferenceTitle-text": {
                        "name": "chatMessageReferenceTitle-text",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#aaafb5", "light": "#9a8eb5"},
                    },
                    "chatfaq-color-chatPlaceholder-text": {
                        "name": "chatPlaceholder-text",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#dfdaea", "light": "rgba(2, 12, 28, .6)"},
                    },
                    "chatfaq-color-clipboard-text": {
                        "name": "clipboard-text",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#cac2da", "light": "#9a8eb5"},
                    },
                    "chatfaq-color-darkFilter": {
                        "name": "darkFilter",
                        "section": "colors",
                        "type": "color",
                        "value": "rgba(2, 12, 28, .7)",
                    },
                    "chatfaq-color-loader": {
                        "name": "loader",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#FFFFFF", "light": "#463075"},
                    },
                    "chatfaq-color-menu-background": {
                        "name": "menu-background",
                        "section": "colors",
                        "type": "gradient",
                        "value": "linear-gradient(135deg, #463075 0%, #220D44 100%)",
                    },
                    "chatfaq-color-menu-border": {
                        "name": "menu-border",
                        "section": "colors",
                        "type": "color",
                        "value": "#4D4160",
                    },
                    "chatfaq-color-menu-scrollColor": {
                        "name": "menu-scrollColor",
                        "section": "colors",
                        "type": "color",
                        "value": "#9FFFFF",
                    },
                    "chatfaq-color-menu-text": {
                        "name": "menu-text",
                        "section": "colors",
                        "type": "color",
                        "value": "#FFFFFF",
                    },
                    "chatfaq-color-menuButton-background": {
                        "name": "menuButton-background",
                        "section": "colors",
                        "type": "color",
                        "value": "#463075",
                    },
                    "chatfaq-color-menuItem-background": {
                        "name": "menuItem-background",
                        "section": "colors",
                        "type": "color",
                        "value": "rgba(223, 218, 234, .1)",
                    },
                    "chatfaq-color-menuItem-background-hover": {
                        "name": "menuItem-background-hover",
                        "section": "colors",
                        "type": "color",
                        "value": "#1A0438",
                    },
                    "chatfaq-color-menuItem-border-edit": {
                        "name": "menuItem-border-edit",
                        "section": "colors",
                        "type": "color",
                        "value": "#9FFFFF",
                    },
                    "chatfaq-color-scrollBar": {
                        "name": "scrollBar",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#463075", "light": "#FFFFFF"},
                    },
                    "chatfaq-color-separator": {
                        "name": "separator",
                        "section": "colors",
                        "type": "color",
                        "value": {"dark": "#4D4160", "light": "rgba(70, 48, 117, .2)"},
                    },
                    "chatfaq-font-body-m": {
                        "name": "body-m",
                        "section": "body",
                        "type": "font",
                        "value": "normal normal 400 24px/33px 'Open Sans'",
                    },
                    "chatfaq-font-body-m-bold": {
                        "name": "body-m-bold",
                        "section": "body",
                        "type": "font",
                        "value": "normal normal 600 16px/22px 'Open Sans'",
                    },
                    "chatfaq-font-body-s": {
                        "name": "body-s",
                        "section": "body",
                        "type": "font",
                        "value": "normal normal 400 14px/19px 'Open Sans'",
                    },
                    "chatfaq-font-body-xl": {
                        "name": "body-xl",
                        "section": "body",
                        "type": "font",
                        "value": "normal normal 400 24px/33px 'Open Sans'",
                    },
                    "chatfaq-font-body-xs": {
                        "name": "body-xs",
                        "section": "body",
                        "type": "font",
                        "value": "normal normal 400 14px/19px 'Open Sans'",
                    },
                    "chatfaq-font-button": {
                        "name": "button",
                        "section": "button",
                        "type": "font",
                        "value": "normal normal 600 14px/17px 'Montserrat'",
                    },
                    "chatfaq-font-caption-md": {
                        "name": "caption-md",
                        "section": "caption",
                        "type": "font",
                        "value": "italic normal 600 14px/19px 'Open Sans'",
                    },
                    "chatfaq-font-caption-sm": {
                        "name": "caption-md",
                        "section": "caption",
                        "type": "font",
                        "value": "normal normal 400 12px/16px 'Open Sans'",
                    },
                    "chatfaq-font-title-l": {
                        "name": "title-l",
                        "section": "title",
                        "type": "font",
                        "value": "normal normal 700 48px/59px 'Montserrat'",
                    },
                    "chatfaq-font-title-sm": {
                        "name": "title-sm",
                        "section": "title",
                        "type": "font",
                        "value": "normal normal 700 24px/29px 'Montserrat'",
                    },
                    "chatfaq-font-title-xl": {
                        "name": "title-xl",
                        "section": "title",
                        "type": "font",
                        "value": "normal normal 700 56px/68px 'Montserrat'",
                    },
                    "chatfaq-font-title-xs": {
                        "name": "title-xs",
                        "section": "title",
                        "type": "font",
                        "value": "normal normal 700 18px/22px 'Montserrat'",
                    },
                    "chatfaq-size-bubbleButton": {
                        "name": "chatfaq-size-bubbleButton",
                        "section": "sizes",
                        "type": "size",
                        "value": "normal normal 600 14px/17px 'Montserrat'",
                    },
                }
            ),
        ),
    ]
