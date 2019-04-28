# WAPY

`WAPY` is an abbreviation of the term `Window Analysis of Products Yourself`, as our entire project evolves around the process of analysing products in your storefront window. The `Yourself` part is included as the entire process is done by the end-user themselves without the need for external  assistance. Tasks ranging from installing the camera in the window, to calibration, to understanding the analytical data fed to their dashboard.

### Architecture

<img width="868" alt="Screen Shot 2019-04-28 at 15 54 36" src="https://user-images.githubusercontent.com/17438617/56864683-18194700-69ce-11e9-81a5-3a2827c8e1b3.png">

### Software and Technologies

- **The Box:** Contains a small computer with 4GB RAM which will be running the following services:
  - Calibration Service - A service which is in charge of communicating with the application via Bluetooth LE in order to setup the other services and authenticate the box.
  - Camera Service - The service which will process the input data from the camera sensor and save the result dispatched to AWS Kinesis, a self managed messaging queue which has it's input consumed by AWS Lambdas.
  - Delivery Service - Is the service which is activated only after calibration. It connects to our remote server, checks and manages updates and makes sure the other services are always running.

- **iOS App:** Built with Swift 4.2, and makes use of [ARKit](https://developer.apple.com/arkit/), as well as [Vision](https://developer.apple.com/documentation/vision) to calibrate the camera's position in respect to the window. In addition to calibration, the app will also serve us as a gateway to send remote notifications for updates, as well as display basic analytical data within the app itself.

- **The Backend:** We have two primary backends, one running on `Java 1.8` and is based on `Jetty`, and Firebase. Each backend serves a different purpose. The Jetty server is in charge of quering the data which is sent from the camera client service, While Firebase is in charge of serving and handling requests from the frontend application on which we will display the analytical data that was processed to the end user.

- **Frontend:** For the frontend we decided to go with the `Angular 6` framework, which we will build using Typescript, HTML, and SCSS. In addition to Angular, we will also use `D3` to visualise results.

- **Databases:** For this task we decided to go with `MySQL` running on AWS RDS and `Firestore`. Where MySQL will store all raw data used for processing, and Firestore will store data which considers the users as well as active sessions. 
