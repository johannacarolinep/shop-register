# Shop Register

Description

Link to [Shop Register](https://shop-register-ce8149331475.herokuapp.com/)

## User stories

## Instructions

## Flowcharts

## Technologies used
### Languages:

- [Python 3.12.1](https://www.python.org/downloads/release/python-385/): used to write the application logic

- [JavaScript](https://www.javascript.com/): was provided as part of the template for the project.

- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML): was provided as part of the template for the project.

### Frameworks/Libraries, Programmes and Tools:
#### Python modules/packages:

##### Standard library imports:

- [os](https://docs.python.org/3/library/os.html): was used to clear the terminal, to provide a better user experience.
- [re](https://docs.python.org/3/library/re.html): was used to write regex expressions for validation of data formats
- [datetime](https://docs.python.org/3/library/datetime.html): was used to generate the current date, as well as for validation of inputted dates

##### Third-party imports:

- [gspread](https://pypi.org/project/gspread/): was used to connect, create, read, update and delete data in a Google Sheet
- [google-auth](https://pypi.org/project/google-auth/): was used to authenticate access to Google Sheet from the application
- [Simple Terminal Menu](https://pypi.org/project/simple-term-menu/): was used to implement all menus in the program.
- [Colorama](https://pypi.org/project/colorama/): was used to add colors to the program.
- [PrettyTable](https://pypi.org/project/prettytable/): was used to print data in a table format in the application.


#### Other tools:

- [VSCode](https://code.visualstudio.com/): was used as the IDE.
- [Git](https://git-scm.com/): was used for version control.
- [GitHub](https://github.com/): was used to host the code of the website.
- [Draw.io](https://www.drawio.com/): was used to make flowcharts of the application.
- [Heroku.com](https://id.heroku.com/login): was used to deploy the project.
- [Google Sheets](https://www.google.com/sheets/about/): was used to store the data.

## Deployment
The program was deployed to [Heroku](https://id.heroku.com/login) and can be accessed by this [link](https://shop-register-ce8149331475.herokuapp.com/).

### To run the application locally:

*Note:*
1. This project requires you to have Python 3 installed on your computer.

2. In order to run the project you will need to install and run [virtualenv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/). This is due to compatibility issues between some versions of Python, such as 3.9.6 and the version of Python run on Heroku.

Create a local copy of the GitHub repository by following one of the two processes below:

- Download ZIP file:
  1. Go to the [GitHub Repository](https://github.com/johannacarolinep/shop-register).
  2. Download the ZIP file containing the project.
  3. Extract the ZIP file to a location on your computer.

- Clone the repository:
  1. Run the following command in a terminal
  - `git clone git@github.com:johannacarolinep/shop-register.git`

### Run the project as a remote web application by deploying to Heroku:

- Clone the repository:
  1. Open a folder on your computer with the terminal.
  2. Run the following command
  - `git clone git@github.com:johannacarolinep/shop-register.git`

  3. Create your own GitHub repository to host the code.
  4. Run the command `git remote set-url origin <Your GitHub Repo Path>` to set the remote repository location to your repository.

  5. Push the files to your repository with the following command:
  `git push`
  
  6. Create a Heroku account if you don't already have one here [Heroku](https://dashboard.heroku.com).
  7. Create a new Heroku application on the [Heroku Apps page](https://dashboard.heroku.com/apps), by clicking "New" in the upper right corner, and selecting "Create new app":

    ![Heroku Apps - New](documentation/heroku-apps-new.png)

8. Name the app, choose a region, and click "Create app".
    ![Heroku New App - Create](documentation/heroku-apps-create.png)

9. Go to the Deploy tab:
    ![Heroku - Deploy Tab](documentation/heroku-deploy-tab.png)

10. In the "Deployment method" section, click on "GitHub - Connect to Github". Search for your repository and connect your application.
    ![Heroku - Connect to GitHub](documentation/heroku-connect-github.png)

  11. Next, go to the Settings tab:
  ![Heroku - Settings tab](documentation/heroku-settings-tab.png)

  12. In the "Buildpacks" section, click "Add buildpack". Then add "python" and "nodejs", in that order (OBS! The order is important.) 
  ![Heroku - Add buildpack](documentation/heroku-buildpacks-section.png)

  ![Heroku - Add python and nodejs](documentation/heroku-add-buildpacks.png)

  ![Heroku - Add python and nodejs](documentation/heroku-buildpacks-order.png)

  13. Next, in the "Config Vars" section, click "Click "Reveal Config Vars". You will need to add 2 Config Vars
  ![Heroku - Reveal Config Vars button](documentation/heroku-reveal-config-vars-btn.png)

- Config Var nr 1:
    - Key: PORT Value: 8000 
    - This Config Var was provided by [CODE INSTITUTE](https://codeinstitute.net/)

- Config Var nr 2:
    - Key: CREDS Value: (Reach out for this value)
    - This Config Var contains the credentials necessary for accessing the Google Sheet linked to the program.
    ![Heroku - Config Vars](documentation/heroku-config-vars.png)

  14. Go back to the Deploy tab:

      ![Heroku - Deploy Tab](documentation/heroku-deploy-tab.png)

  17. In the "Manual deploy" section, click "Deploy Branch":

      ![Heroku - Manual deploy](documentation/heroku-manual-deploy.png)

      - Wait for the completion of the deployment.

      ![Heroku - Manual deployment success](documentation/heroku-deployment-success.png)

  18. You can now click the "View" button (in the screenshot above), to launch the application.


## Testing
All test-related documentation can be found in [TESTING.md](TESTING.md).

## Bugs
### Solved bugs
### Unsolved bugs



## Credits
- [gspread](https://pypi.org/project/gspread/) and [google-auth](https://pypi.org/project/google-auth/) - connection to Google Sheet
- [Simple Terminal Menu](https://pypi.org/project/simple-term-menu/) - Terminal menus
- [Colorama](https://pypi.org/project/colorama/) - color formatting
- [PrettyTable](https://pypi.org/project/prettytable/) - table printouts

## Acknowledgements
