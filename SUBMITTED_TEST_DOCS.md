## Discrepancy Checker

New endpoint can be found at "/company/validate-pdf-data".

The endpoint expects a company name query parameter and a pdf file.
The response looks roughly as follows:
```json
{
  "uploaded_data": {
    "extracted data from pdf": "..."
  },
  "stored_data": { 
     "existing data stored on this service": "..."
  },
  "mismatched_fields": [
    {
      "field_name": "...",
      "uploaded_value": "...",
      "stored_value": "..."
    }]
}
```

To run tests locally, the ENVIRONMENT environment variable needs to be set to TEST:
`export ENVIRONEMNT=TEST`


## Assumptions
- User provides company name (assumed missing punctuation in README :) ), along with a pdf file.
- The company name should match an existing record, otherwise 400 error is returned.
- PDF Service is an external microservice (with only 3 possible outputs) and is outside of scope.
- Used decimal typing for all numeric fields (except for _number_of_employees_ which can safely be assumed as an int)
- Assumed _net_income_margin_, _current_ratio_, _ceo_ and _number_of_employees_ to be optional based on provided test data
- Response should include both sets of company data and mismatched fields.


## Future Work

To go into production we would want a database setup and some proper authentication.
The current response is also quite verbose which is helpful for initial development but could be slimmed down later on.

### Database

In addition to the stored company data, we need a db record of pdf files uploaded to the endpoint. 
This record could contain company name, extracted data, file path (pointing to a bucket or similar) and a hash of the pdf contents.
The hash could be used to check if an identical file had been previously uploaded for the same company, so we only extract data where necessary.

This table could exist on either the pdf service, on the data checker or even on both (depending on how each service is used). 
Having it on the pdf service seems more intuitive, but having it on the data checker service means we would only need to call 
the pdf service for new files, thus reducing requests between services. 

### Authentication

In production we could setup the deployment pipeline (e.g. via GitHub actions) to store the api_key for pdf_service as an environment variable to be fetched when the code runs in production.
The config file shows how that api_key would be used.
We also might want proper user authentication on the data checker endpoint. Again, we would need a db for this and would need the service to generate and store a token for the user to provide in the request header.


### Data Validation

Some of the fields like location are almost a match. We could add more sophisticated logic there to do partial matching on things like location if we really wanted to.
We could also use rounding when matching numeric values.

