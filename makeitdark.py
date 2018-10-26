from sys import platform
import os

injectable = "document.addEventListener(\"DOMContentLoaded\", function() {  \n\
   \n\
    /* Then get its webviews */  \n\
    let webviews = document.querySelectorAll(\".TeamView webview\");  \n\
   \n\
    /* Fetch CSS in parallel ahead of time from cdn host */  \n\
    const cssPath = 'https://raw.githubusercontent.com/techwithjake/dark_slack_mode/master/dark_slack.css';  \n\
    let cssPromise = fetch(cssPath).then(response => response.text());  \n\
   \n\
    let customCustomCSS = `  \n\
    :root {  \n\
        /* Modify these to change your theme colors: */  \n\
        --primary: #61AFEF;  \n\
        --text: #ededed;  \n\
    }  \n\
    div.c-message.c-message--light.c-message--hover {  \n\
        color: #ededed !important;  \n\
    }  \n\
   \n\
    a.c-message__sender_link { color: #61AFEF !important; }  \n\
   \n\
    span.c-message__body, span.c-message_attachment__media_trigger.c-message_attachment__media_trigger--caption,  \n\
    div.p-message_pane__foreword__description span {  \n\
        color: #ededed !important;  \n\
        font-family: \"Fira Code\", Arial, Helvetica, sans-serif;  \n\
        text-rendering: optimizeLegibility;  \n\
        font-size: 14px;  \n\
    }  \n\
   \n\
    div.c-virtual_list__scroll_container {  \n\
        background-color: #080808 !important;  \n\
    }  \n\
   \n\
    .p-message_pane .c-message_list:not(.c-virtual_list--scrollbar),  \n\
    .p-message_pane .c-message_list.c-virtual_list--scrollbar > .c-scrollbar__hider {  \n\
        z-index: 0;  \n\
    }  \n\
   \n\
   \n\
    div.c-message__content:hover {  \n\
        background-color: #080808 !important;  \n\
    }  \n\
   \n\
    div.c-message:hover {  \n\
        background-color: #080808 !important;  \n\
    }`  \n\
   \n\
    /* Insert a style tag into the wrapper view */  \n\
    cssPromise.then(css => {  \n\
        let s = document.createElement('style');  \n\
        s.type = 'text/css';  \n\
        s.innerHTML = css + customCustomCSS;  \n\
        document.head.appendChild(s);  \n\
    });  \n\
   \n\
    /* Wait for each webview to load */  \n\
    webviews.forEach(webview => {  \n\
        webview.addEventListener('ipc-message', message => {  \n\
            if (message.channel == 'didFinishLoading')  \n\
            /* Finally add the CSS into the webview */  \n\
            cssPromise.then(css => {  \n\
                let script = `  \n\
                    let s = document.createElement('style');  \n\
                    s.type = 'text/css';  \n\
                    s.id = 'slack-custom-css';  \n\
                    s.innerHTML = \`${css + customCustomCSS}\`;  \n\
                    document.head.appendChild(s);  \n\
                `  \n\
                webview.executeJavaScript(script);  \n\
            })  \n\
        });  \n\
    });  \n\
});"

slack_theme_path = ""

if platform == "linux" or platform == "linux2":
    # linux
    print("Detected linux OS")
    slack_theme_path = "/usr/lib/slack/resources/app.asar.unpacked/src/static/ssb-interop.js"
elif platform == "darwin":
    # OS X
    print("Detected OS X")
    slack_theme_path = "/Applications/Slack.app/Contents/Resources/app.asar.unpacked/src/static/ssb-interop.js"
else:
    # Probably Windows
    slack_root_path = os.path.join(os.environ['LOCALAPPDATA'], "slack")
    most_recent = sorted([slack_version for slack_version in os.listdir(slack_root_path) if slack_version.startswith("app-") and os.path.isdir(os.path.join(slack_root_path, slack_version))], reverse=True)[0]
    print("Searching for most recent slack update in {0}".format(slack_root_path))
    print("Found {0}".format(most_recent))
    slack_theme_path = os.path.join(slack_root_path, most_recent, "resources", "app.asar.unpacked", "src", "static", "ssb-interop.js")

f = open(slack_theme_path, "a+")
f.write("\n" + injectable)
f.close()
print("Your slack theme has been updated, please restart slack")
exit()
