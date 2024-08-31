from website import create_app
# import time #temporary clock
# from datetime import datetime #continue

app = create_app ()
# currentTime = datetime.now().time()


if __name__ == '__main__':
    # app.run (debug = True)
    app.run(host='0.0.0.0', port=5000, debug = True)
    