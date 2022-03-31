from flaskr import create_app

app = create_app()

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=8080,debug=True)

# for AWS Elastic Beanstalk => application!
application=app
if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8080,debug=True)