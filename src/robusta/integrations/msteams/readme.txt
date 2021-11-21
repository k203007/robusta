The msteams message mechanism is based on Msteams Adaptive card.

Python has an old package for Adaptive card, and a newer package to create a basic card which is 

not suitable for our needs.

the link for the the adaptive card is: https://adaptivecards.io/explorer/

The markdown explanation for adaptive card: https://docs.microsoft.com/en-us/microsoftteams/platform/task-modules-and-cards/cards/cards-format?tabs=adaptive-md%2Cconnector-html

Note that the markdown is limited.

The max msg size is ~28K but there isn't a definite model to calculate it so we take msg of up to 20K.

The size of the url is not included in the calculation (we put the image base 64 inside the url)

Most of the actions are not supported by msteams such as action.submit and execute.

Calling url with body doesn't seem possible, instead use url with query parameters, and call the url with the action url.

The fastest way to debug the msteams is using postman, where you send a post request using the webhook url.

NOTE:  that there is no option to upload files to sharepoint with msteams webhook !!!

