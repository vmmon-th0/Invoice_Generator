# invoice_generator

Automate the creation and management of invoices for a business or freelancer. The application allows users to input client information, products or services provided, quantities, and rates, then generates an invoice in PDF or other formats. It may include features such as automatic tax calculation, payment tracking, and invoice storage for streamlined financial management.

## Invoice preview :
![alt text](https://i.imgur.com/ShPyniT.png)

WIP, soon making a GUI would be a great step forward, a local python webservice.
TODO :

## Structure of our data (JSON)

```
{
    "my_info": {
      "name": "Ammon Schiffer",
      "address": "5 random avenue",
      "city": "75001 somewhere",
      "phone": "+33 6 23 45 67 89",
      "email": "example@gmail.com",
      "SIRET": "12345678912345",
      "VAT_number": "FR12345678912"
    },
    "client_info": {
      "name": "GITHUB CORP",
      "address": "6 random avenue",
      "city": "75001 somewhere",
      "phone": "01 71 05 38 32",
      "email": "example@gmail.com",
      "SIRET": "12345678912345",
      "VAT_number": "FR12345678912"
    },
    "prestations": [
      {
        "id": "1",
        "description": "Fullstack Engineering",
        "unit": "Day",
        "quantity": 20,
        "price": 500.00,
        "VAT_PCT": 0
      },
      {
        // etc.
      }
    ]
}
```

## TODO

The idea would be to have a local environment that will support:

- Create JSON standart + doc

- Create .conf file for local dev

- More informations about prestations

- Sales tracking, data can be stored in storage as on a third party DB.

- A minimalist interface accepting only inputs, design management is static.

- Improve design by alignment.

- VAT activation/deactivation.

- A backup on an external cloud.

I really insist on the fact that this is a local, open-source service.
