# Generated by Django 4.1.13 on 2023-11-27 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Widget",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("domain", models.URLField()),
                ("fsm_name", models.CharField(max_length=255)),
                (
                    "layout",
                    models.CharField(
                        choices=[("regular", "Regular"), ("full", "Full screen")],
                        default="regular",
                        max_length=255,
                    ),
                ),
                ("history_opened", models.BooleanField(default=False)),
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                ("subtitle", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Theme",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "data",
                    models.JSONField(
                        default={
                            "chatfaq-color-alertMessage-text": {
                                "defaults": {"dark": "#e7e8e9", "light": "#545a64"},
                                "name": "chatfaq-color-bubbleButton-background-hover",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-bubbleButton-background": {
                                "default": "linear-gradient(135deg, #CE0578 0%, #463075 100%)",
                                "name": "chatfaq-color-bubbleButton-background",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-bubbleButton-background-hover": {
                                "default": "linear-gradient(135deg, #463075 0%, #220D44 100%)",
                                "name": "chatfaq-color-bubbleButton-background-hover",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-chat-background": {
                                "defaults": {"dark": "#4D4160", "light": "#dfdaea"},
                                "name": "chatfaq-color-chat-background",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-chatInput-background": {
                                "defaults": {"dark": "#3c2d52", "light": "#cac2da"},
                                "name": "chatfaq-color-chatInput-background",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-chatInput-border": {
                                "defaults": {"dark": "#1A0438", "light": "#9a8eb5"},
                                "name": "chatfaq-color-chatInput-border",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-chatInput-text": {
                                "defaults": {"dark": "#FFFFFF", "light": "#020C1C"},
                                "name": "chatfaq-color-chatInput-text",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-chatMessageBot-background": {
                                "defaults": {"dark": "#3c2d52", "light": "#cac2da"},
                                "name": "chatfaq-color-chatMessageBot-background",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-chatMessageBot-text": {
                                "defaults": {"dark": "#FFFFFF", "light": "#020C1C"},
                                "name": "chatfaq-color-chatMessageBot-text",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-chatMessageHuman-background": {
                                "defaults": {"dark": "#1A0438", "light": "#463075"},
                                "name": "chatfaq-color-chatMessageHuman-background",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-chatMessageHuman-text": {
                                "defaults": {"dark": "#FFFFFF", "light": "#FFFFFF"},
                                "name": "chatfaq-color-chatMessageHuman-text",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-chatMessageReference-background": {
                                "defaults": {
                                    "dark": "#1A0438",
                                    "light": "rgba(70, 48, 117, .1)",
                                },
                                "name": "chatfaq-color-chatMessageReference-background",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-chatMessageReference-text": {
                                "defaults": {"dark": "#dfdaea", "light": "#463075"},
                                "name": "chatfaq-color-chatMessageReference-text",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-chatMessageReferenceTitle-text": {
                                "defaults": {"dark": "#aaafb5", "light": "#9a8eb5"},
                                "name": "chatfaq-color-chatMessageReferenceTitle-text",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-chatPlaceholder-text": {
                                "defaults": {
                                    "dark": "#dfdaea",
                                    "light": "rgba(2, 12, 28, .6)",
                                },
                                "name": "chatfaq-color-chatPlaceholder-text",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-clipboard-text": {
                                "defaults": {"dark": "#cac2da", "light": "#9a8eb5"},
                                "name": "chatfaq-color-clipboard-text",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-darkFilter": {
                                "default": "rgba(2, 12, 28, .7)",
                                "name": "chatfaq-color-darkFilter",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-loader": {
                                "defaults": {"dark": "#FFFFFF", "light": "#463075"},
                                "name": "chatfaq-color-loader",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-menu-background": {
                                "default": "linear-gradient(135deg, #463075 0%, #220D44 100%)",
                                "name": "chatfaq-color-menu-background",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-menu-border": {
                                "default": "#4D4160",
                                "name": "chatfaq-color-menu-border",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-menu-scrollColor": {
                                "default": "#9FFFFF",
                                "name": "chatfaq-color-menu-scrollColor",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-menu-text": {
                                "default": "#FFFFFF",
                                "name": "chatfaq-color-menu-text",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-menuButton-background": {
                                "default": "#463075",
                                "name": "chatfaq-color-menuButton-background",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-menuItem-background": {
                                "default": "rgba(223, 218, 234, .1)",
                                "name": "chatfaq-color-menuItem-background",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-menuItem-background-hover": {
                                "default": "#1A0438",
                                "name": "chatfaq-color-menuItem-background-hover",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-menuItem-border-edit": {
                                "default": "#9FFFFF",
                                "name": "chatfaq-color-menuItem-border-edit",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-scrollBar": {
                                "defaults": {"dark": "#463075", "light": "#FFFFFF"},
                                "name": "chatfaq-color-scrollBar",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-color-separator": {
                                "defaults": {
                                    "dark": "#4D4160",
                                    "light": "rgba(70, 48, 117, .2)",
                                },
                                "name": "chatfaq-color-separator",
                                "section": "colors",
                                "type": "color",
                            },
                            "chatfaq-font-body-m": {
                                "default": "normal normal 400 24px/33px 'Open Sans'",
                                "name": "chatfaq-font-body-m",
                                "section": "body",
                                "type": "font",
                            },
                            "chatfaq-font-body-m-bold": {
                                "default": "normal normal 600 16px/22px 'Open Sans'",
                                "name": "chatfaq-font-body-m-bold",
                                "section": "body",
                                "type": "font",
                            },
                            "chatfaq-font-body-s": {
                                "default": "normal normal 400 14px/19px 'Open Sans'",
                                "name": "chatfaq-font-body-s",
                                "section": "body",
                                "type": "font",
                            },
                            "chatfaq-font-body-xl": {
                                "default": "normal normal 400 24px/33px 'Open Sans'",
                                "name": "chatfaq-font-body-xl",
                                "section": "body",
                                "type": "font",
                            },
                            "chatfaq-font-body-xs": {
                                "default": "normal normal 400 14px/19px 'Open Sans'",
                                "name": "chatfaq-font-body-xs",
                                "section": "body",
                                "type": "font",
                            },
                            "chatfaq-font-button": {
                                "default": "normal normal 600 14px/17px 'Montserrat'",
                                "name": "chatfaq-font-button",
                                "section": "button",
                                "type": "font",
                            },
                            "chatfaq-font-caption-md": {
                                "default": "italic normal 600 14px/19px 'Open Sans'",
                                "name": "chatfaq-font-caption-md",
                                "section": "caption",
                                "type": "font",
                            },
                            "chatfaq-font-caption-sm": {
                                "default": "normal normal 400 12px/16px 'Open Sans'",
                                "name": "chatfaq-font-caption-md",
                                "section": "caption",
                                "type": "font",
                            },
                            "chatfaq-font-title-l": {
                                "default": "normal normal 700 48px/59px 'Montserrat'",
                                "name": "chatfaq-font-title-l",
                                "section": "title",
                                "type": "font",
                            },
                            "chatfaq-font-title-sm": {
                                "default": "normal normal 700 24px/29px 'Montserrat'",
                                "name": "chatfaq-font-title-sm",
                                "section": "title",
                                "type": "font",
                            },
                            "chatfaq-font-title-xl": {
                                "default": "normal normal 700 56px/68px 'Montserrat'",
                                "name": "chatfaq-font-title-xl",
                                "section": "title",
                                "type": "font",
                            },
                            "chatfaq-font-title-xs": {
                                "default": "normal normal 700 18px/22px 'Montserrat'",
                                "name": "chatfaq-font-title-xs",
                                "section": "title",
                                "type": "font",
                            },
                            "chatfaq-size-bubbleButton": {
                                "default": "normal normal 600 14px/17px 'Montserrat'",
                                "name": "chatfaq-size-bubbleButton",
                                "section": "sizes",
                                "type": "size",
                            },
                        }
                    ),
                ),
                (
                    "widget",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="widget.widget"
                    ),
                ),
            ],
        ),
    ]
