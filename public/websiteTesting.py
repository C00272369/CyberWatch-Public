from flask import Flask, session, render_template, request
import cwTools
import time, threading

 #↓ Sets application variable to file name?
cyber_watch = Flask(__name__)
cyber_watch.secret_key = "TempPass"

 #↓ Threaded function which periodically updates the posts_ordered list.
def auto_update_posts():
    global posts_ordered
    while True:
        posts_ordered = cwTools.update_posts()
        time.sleep(3600)

 #↓ Start the thread process
threading.Thread(target=auto_update_posts, daemon=True).start()

 #↓ Sets the root route to send the user to the news page.
@cyber_watch.route("/")
def news():
     #↓ Display the news page, and bring posts_ordered with it.
    return render_template('news.html', posts=posts_ordered)

if __name__ == '__main__':
    #↓ Start website server
   cyber_watch.run(debug = True)