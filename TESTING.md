# Testing of Shop Register
## Manual testing

### Testing of the primary menus

<details>
<summary>Click here to see manual testing of the MAIN MENU, INVENTORY MENU and SALES MENU.</summary>

| __Test case__ | __Action__ | __Expected outcome__ | __Pass?__ | __Comments__ |
| ------------- | -----------| -------------------- | :-------: | ------------ |
| Program start | n/a | Displays welcome message and main menu | Y | - |
| Main menu | Move selector between menu options with up/down arrows | Selector is moved when pressing up and down arrows | Y | - |
|           | Press enter while option "1. Inventory" is selected | The inventory menu displays | Y | - |
|           | Press enter while option "2. Sales" is selected | The sales menu displays | Y | - |
|           | Press enter while option "3. Quit" is selected | The quit message displays and the program is quit | Y | - |
| Inventory menu | Move selector between menu options with up/down arrows | Selector is moved when pressing up and down arrows | Y | - |
|                | Select option *1. Display inventory* | Display inventory path is launched* | Y | - |
|                | Select option *2. Look up article* | *Look up article* path is launched* | Y | - |
|                | Select option *3. Add article* | *Add article* path is launched* | Y | - |
|                | Select option *4. Edit article* | *Edit article* path is launched* | Y | - |
|                | Select option *5. Delete article* | *Delete article* path is launched* | Y | - |
|                | Select option *6. Back to main menu* | The main menu is displayed | Y | - |
| Sales menu | Move selector between menu options with up/down arrows | Selector is moved when pressing up and down arrows | Y | - |
|            | Select option *1. Display orders (by date)* | *Display order history* path is launched* | Y | - |
|            | Select option *2. Look up order by ID* | *Look up order by ID* path is launched* | Y | - |
|            | Select option *3. Register an order* | *Register order* path is launched | Y | - |
|            | Select option *4. Back to main menu* | The main menu is displayed | Y | - |

*Meaning the path header is printed (title and brief explanation), and the correct next step is initiated, eg. the user is asked for input.

</details>

### Testing of the Inventory paths of the program

<details>
<summary>Click here to see manual testing of the INVENTORY part or the program</summary>

| __Test case__ | __Action__ | __Expected outcome__ | __Pass?__ | __Comments__ |
| ------------- | -----------| -------------------- | :---------: | ------------ |
| __Display inventory__ | n/a | After header is printed, prints the full shop inventory in table | Y | - |
|                   | Displaying inventory when articles have values of maximum length (name 34 characters, quantity 99999 etc) | Table format is not broken | Y | - |
|                   | Pressing enter | Terminal clears and main menu is displayed | Y | - |
| __Look up article__ | n/a | After header is printed, user is asked to input article number | Y | - |
|                 | enter input for article number | Input is validated according to validation for article numbers (see below). Program keeps asking until input is valid. | Y | - |
|                 | input valid article which does not exist "2000" | User informed article not found. Path end menu is printed | Y | - |
|                 | input valid article which exists "1001" | Article details for article 1001 is printed in a table. Path end menu is printed | Y | - |
| Look up article path end menu | Select *Look up another article* | *Look up article* path restarts | Y | - |
|                               | Select *Back to main menu* | Terminal cleared and the main menu is displayed | Y | - |
| __Add article__ | n/a | After header is printed, user is asked to input article number | Y | - |
|             | enter input for article number | Input is validated according to validation for article numbers (see below). Program keeps asking until input is valid. | Y | - |
|             | enter article number which exists in inventory "1001" | User is informed and asked to edit article instead | Y | - |
|             | Select *Yes* when asked to edit article instead | Terminal cleared and the *Edit article* path is launched, with the selected article pre-filled | Y | - |
|             | Select *No* when asked to edit article instead | *Add article* path end menu is printed | Y | - | 
|             | enter article number which exists in *inactive articles* "1004" | User is informed article number belongs to an inactive article. *Add article* path end menu is printed | Y | - |
|             | enter valid article number that does not exist | Progress indication table is printed with article number. User is asked for article name | Y | - |
|             | enter input for article name | Input is validated for article name (see below). Program keeps asking until valid input is entered. | Y | - |
|             | enter valid article name | Progress indication table is printed with name filled in. User is asked for the *price in* | Y | - |
|             | enter input for *price in* | Input is validated for *price* (see below). Program keeps asking until valid input is entered. | Y | - |
|             | input for *price in* is 500 or above, but below absolute upper limit | User is asked to confirm. | Y | - |
|             | Select No (You entered 501.0. Are you sure?) | User is informed price is not registered. Asked to input *price in* again | Y | - |
|             | Select Yes (You entered 501.0. Are you sure?) | Value is accepted for *price in* | Y | - |
|             | enter valid input for *price in*, below 500 | Value is accepted. Progress indication table is printed with *price in* filled in. User is asked to enter *price out* | Y | - |
|             | enter input for *price out* | Input is validated for *price* (see below). Program keeps asking until valid input is entered. | Y | - |
|             | enter valid input for *price out* that is greater than *price in* | User is asked to confirm | Y | - |
|             | confirm *price out* (greater than *price in*) | Value accepted, and progress indication table is printed with *price out* filled in. User is asked to enter quantity. |
|             | answer "No" when asked to confirm *price out* | Asks for new input for *price out* | Y | - |
|             | enter valid input for *price out*, but 500+ | User is asked to confirm | Y | - |
|             | Enter valid input for *price out*, higher than *price in*, and below 500 | Value accepted, progress indication table is printed with *price out* filled in. User is asked for stock quantity | Y | - |
|             | Enter input for *quantity* | Input is validated for *quantity* (see below). Program keeps asking until valid input is entered | Y | - |
|             | Enter valid input for *quantity* eg "7" | Input is accepted. The finished article's details are printed in a table. A green success message is printed. The article is added to the inventory sheet. The *add article* path end menu is printed | Y | - |
| Add article path end menu | Select *Add another article* | Restarts the *Add article* path | Y | - |
|                           | Select *Back to main menu* | Terminal clears and the main menu is printed | Y | - |
| __Edit articles__ | n/a | After header is printed, user is asked to input article number | Y | - |
|               | enter input for article number | Input is validated according to validation for article numbers (see below). Program keeps asking until input is valid. | Y | - |
|               | input valid article number, but which is not in inventory | User informed article not found. *Edit article* path end menu is printed | Y | - |
|               | input valid article number which exists in inventory | Article details are printed. User is asked to confirm if they want to edit the article | Y | - | 
|               | Select "No" (Would you like to edit this article?) | The *Edit article* path end menu is printed | Y | - |
|               | Select "Yes" (Would you like to edit this article?) | A multi-selection menu is printed. User is asked to select which attributes to edit. | Y | - |
|               | Press up and down arrows | The selector moves between the attribute options in the menu | Y | - |
|               | Press space/tab while in the menu | The highlighted attribute is marked for selection | Y | - |
|               | Press space/tab while on an already marked attribute | The highlighted attribute is un-marked/de-selected | Y | - |
|               | Press enter while no attributes are selected | User is informed no attributes were selected. The *Edit article* path end menu is printed | Y | - |
|               | Press enter while min 1 attribute is selected | User is asked for input for each attribute, in order. Program keeps asking for each input until valid input is entered | Y | - |
|               | Enter valid input for a selected attribute to edit | Green message is printed, confirming the value is updated. The value is updated in the inventory sheet. | Y | - |
|               | Enter valid input for the last selected attribute to edit | After confirmation of updated value, the *Edit article* path end menu is printed | Y | - |
| Edit article path end menu | Select *Edit another article* | *Edit article* path restarts | Y | - |
|                               | Select *Back to main menu* | Terminal cleared and the main menu is displayed | Y | - |
| __Delete article__ | n/a | After header is printed, user is asked to input article number | Y | - |
|                | enter input for article number | Input is validated according to validation for article numbers (see below). Program keeps asking until input is valid. | Y | - |
|                | enter article number which does not exist in inventory | User is informed article not found, and the *Delete article* path end menu is printed | Y | - |
|                | enter article number which exists in inventory | Article details are printed in a table. The user is asked to confirm deletion | Y | - |
|                | Select "Yes" (Would you like to delete this article?) | Confirms to the user the article was removed. The article row is deleted in the inventory sheet, and added in the inactive articles sheet. The *Delete article* path end menu is printed | Y | - |
|                | Select "No" (Would you like to delete this article?) | User is informed the action was cancelled. The *Delete article* path end menu is printed | Y | - |
| Delete article path end menu | Select *Delete another article* | Restarts the *Delete article* path | Y | - |
|                              | Select *Back to main menu* | Terminal clears and the main menu is printed | Y | - |

</details>

### Testing of Sales part of the program

<details>
<summary>Click here to see testing of the SALES part of the program.</summary>

| __Test case__ | __Action__ | __Expected outcome__ | __Pass?__ | __Comments__ |
| ------------- | ---------- | -------------------- | :---------: | ------------ |
| __Display orders by date__ | n/a | After header is printed, user is asked to input START date | Y | - |
|                | enter input for START date | Input is validated according to validation for dates (see below). Program keeps asking until input is valid. | Y | - |
|                | enter valid input for a START date | User is asked to enter input for END date | Y | - |
|                | enter input for END date | Input is validated according to validation for dates and END dates (see below). Program keeps asking until input is valid. | Y | - |
|                | enter valid input for END date | Program checks if there are any orders registered between START and END date in the order history sheet | Y | - |
|                | n/a | If there are no orders between START and END date, informs user of no orders to display. If there are orders between START and END date, prints the orders in a table. The *Display orders by date* path end menu is printed | Y | - |
| Display orders by date path end menu | Select *Search for different dates* | Restarts *Display orders by date* path | Y | - |
|                                      | Select *Back to main menu* | Clears terminal and prints the main menu | Y | - |
| __Look up order by ID__ | n/a | After header is printed, user is asked to input order ID | Y | - |
|                | enter input for *order ID* | Input is validated according to validation for order ID's (see below). Program keeps asking until input is valid. | Y | - |
|                | enter valid *order ID* but which does not exist in order history | User informed there is no order with the provided ID in the system. The *Look up order by ID* path end menu is printed | Y | - |
|                | enter valid *order ID which exists in the order history | The order details is printed in a table together with additional details total order sum and total order quantity. The *Look up order by ID* path end menu is printed | Y | - |
| Look up order by ID path end menu | Select *Search for different order* | Restarts the *Look up order by ID* path | Y | - |
|                                   | Select *Back to main menu* | Terminal is cleared and the main menu is printed | Y | - |
| __Register an order__ | n/a | After header is printed, user is asked to input an article number | Y | - |
|                | enter input for *article number* | Input is validated according to validation for article numbers (see below). Program keeps asking until input is valid. | Y | - |
|                | enter valid *article number* but which does not exist in the inventory | The user is informed and asked to input another article number | Y | - |
|                | enter valid *article number* which exists in inventory | The user is asked for the sales quantity and is given the current stock quantity of the article | Y | - |
|                | enter input for *sales quantity* | Input is validated according to validation for *quantity* and *sales quantity* | Y | - |
|                | enter valid input for *sales quantity* | User is asked if they want to add more rows to the order or complete the order | Y | - |
|                | Select *Add row to sales order* | User is asked for another article number and sales quantity | Y | - |
|                | Select *Order is complete* | The order details are printed in a table. The user is asked to either *Finalize order* or *Cancel order* | Y | - |
|                | Select *Cancel order | The *Register order* path end menu is printed | Y | - |
|                | Select *Finalize order | Green message confirms order registration to the user. The order is registered in the order history sheet. The inventory stock level is adjusted for the sold articles. The *Register order* path end menu is printed | Y | - |
| Register order path end menu | Select *Register another order* | Restarts the *Register order* path | Y | - |
|                              | Select *Back to main menu* | Clears terminal and prints the main menu | Y | - |

</details>

### Testing of input validation

<details>
<summary>Click here to see manual testing of INPUT VALIDATION</summary>

| __Test case__ | __Action__ | __Expected outcome__ | __Pass?__ | __Comments__ |
| ------------- | ---------- | -------------------- | :---------: | ------------ |
| __Article number__ | empty input | Feedback message for empty input is printed. User is asked for input again | Y | - |
|                | input string "asfldkh" | Feedback, must be an integer. User asked for input again | Y | - |
|                 | input decimal value "3.5" | Feedback, must be an integer. User asked for input again | Y | - |
|                 | input negative integer "-5" | Feedback, must be positive. User asked for input again | Y | - |
|                 | input integer out of range "10011" | Feedback, must be positive and 4 digits. User asked for input again | Y | - |
|                 | enter valid input "1002" | Input accepted | Y | - |
| __Article name__ | empty input | Feedback message for emply input is printed. Asks for input again. | Y | - |
|              | input only numbers "123456789" | Feedback, incorrect format. User asked for input again. | Y | - |
|              | input only special characters "!"#€%" | Feedback, incorrect format. User asked for input again | Y | - |
|              | input has more than 1 numbers "no3 thing 5" | Feedback, incorrect format. User asked for input again | Y | - |
|              | input is less than 5 characters "ball" | Feedback, min length is 5 | Y | - | 
|              | input is above 34 characters "ball no34 glittery bouncy yellow bouncy ball" | Feedback, max length is 34 | Y | - |
|              | input contains superfluous spaces "    ball  no34  " | Superflous spaces removed and then validates. In this case "ball no34" is valid | Y | Name is stored as "BALL NO34" (uppercase, extra spaces removed) |
|              | enters valid input for name "terrifying t-rex!" | input is accepted | Y | Name is stored as "TERRIFYING T-REX!" (uppercase) |
| __Price__ | empty input | Feedback message for emply input is printed. Asks for input again. | Y | - |
|          | input is not a number | Feedback, must be a decimal number. Asks for input again | Y | - |
|          | input is negative value | Feedback, must be a positive value. Asks for input again | Y | - |
|          | input is 0 | Feedback, must be a positive value. Asks for input again | Y | - |
|          | input is above 99999.99 | Feedback, above the upper limit for a price. Asks for input again | Y | - |
| __Quantity__ | empty input | Feedback message for emply input is printed. Asks for input again. | Y | - |
|          | input is not a number | Feedback, must be an integer. Asks for input again | Y | - |
|          | input is negative value | Feedback, must be a positive value. Asks for input again | Y | - |
|          | input is a decimal value | Feedback, must be an integer. Asks for input again | Y | - |
|          | input is above 999999 | Feedback, above the upper limit for a quantity. Asks for input again | Y | - |
| __Sales quantity__ | input is valid quantity, but greater than current stock level for associated article | Feedback, sales quantity cannot be larger than current stock quantity. Asks for input again. | Y | - | 
| __Date__ | empty input | Feedback message for emply input is printed. Asks for input again. | Y | - |
|      | input is not format YYYY-MM-DD | Feedback, format must be YYYY-MM-DD | Y | - |
|      | input is YYYY-MM-DD, but not a valid date, eg "2023-13-52" | Feedback, date does not exist. Asks for input again | Y | - |
|      | input is valid date, but in the future, eg "2025-01-10" | Feedback, date cannot be greater than current date. Asks for input again | Y | - |
| __END date__ | input is a valid date, but a date before the START date | Feedback, END date cannot come before START date. Asks for input again | Y | - | 
| __Order ID__ | empty input | Feedback message for emply input is printed. Asks for input again. | Y | - |
|          | input is not a number | Feedback, must be an integer. Asks for input again | Y | - |
|          | input is negative value | Feedback, must be a positive value. Asks for input again | Y | - |
|          | input is a decimal value | Feedback, must be an integer. Asks for input again | Y | - |
|          | input is a positive integer, out of range | Feedback, must be a positive 5 digit integer. Asks for input again | Y | - |

</details>

## Validation
Code Institute's CI Python Linter was used to ensure all of project's code is compliant with Pep 8 standards.

By copying all of the code from each file into the tool, I was able to confirm there were no errors found (see screenshots below).

- run.py:
![Linter: run.py](documentation/linter-run.png)

- articles.py:
![Linter: articles.py](documentation/linter-articles.png)

- orders.py:
![Linter: orders.py](documentation/linter-orders.png)

- validators.py:
![Linter: validators.py](documentation/linter-validators.png)

- get_user_input.py:
![Linter: get_user_input.py](documentation/linter-getuserinput.png)

- helpers.py:
![Linter: helpers.py](documentation/linter-helpers.png)

### Empty line at end of file
As can be seen in the screenshots from the CI Python Linter tool, each file has an empty line at the end of the file (in compliance with Pep 8 standards).