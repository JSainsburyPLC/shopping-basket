[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


# shopping-basket
This repository contains a simple shopping basket application that is used as a
Python coding exercise for recruitment purposes. For that reason the code and
tests _may_ be incomplete and (maybe) not all of the tests work! This README
defines a brief for the candidate, and what the _required_ usage and behaviour
of the application is.

## The brief
Your interview at Sainsbury's will contain a technical section. Technical
interviews can feel daunting, that's why we'd like to provide the opportunity
for you to prepare in advance.

You might like to familiarise yourself with the contents of this repository in
preparation for the technical section of your interview. The extent of your
preparation is entirely up to you and should be driven by what you feel suits
you best as an individual. We will want to discuss this application with you,
as well as any observations you may have. Furthermore, at the bottom of this
README is list of some possible future requirements that we might, if time
permits, ask you to have a go at one or more of them.

> NB: This activity is designed for candidates with a wide range of skills and
> experiences. Don't worry if some of the proposed features seem outside of
> your area of expertise, we certainly don't expect everyone to know everything.

We are flexible about the structure of the technical section of the interview.
You may want to bring some fixes, improvements or additions with you and use
those as a starting point. Ideally we would like to pair with you during the
exercise, however if you feel you might get on better when left alone, then
that is also fine - just let us know. The main objective of the exercise is
that we experience the way you work and approach problems in the best possible
light. Good luck!

## Usage
Check out the repo and navigate to `shopping-basket/`.  There are two JSON
data files used by the application.

### products.json
A JSON file that contains a list of all available products that can be added
to a shopping basket. Note that all item prices are in pence.
 
### promotions.json
A JSON file that contains a list of all available promotions that can be
applied to items added to the shopping basket.

Execute as follows to show usage:
```
python -m basket -h
usage: basket [-h] [-v] [--products PRODUCTS] [--promotions PROMOTIONS]
              [--verbose] item [item ...]

positional arguments:
  item             One or more items for the basket. Only items listed in
                   products.json are accepted

optional arguments:
  -h, --help              Show this help message and exit
  -v, --version           Show program's version number and exit
  --verbose               Verbose output
  --products PRODUCTS     Path of the products json file, default is
                          ./products.json
  --promotions PROMOTIONS Path of the promotions json file, default is
                          ./promotions.json  
```

## Examples
```
$ python -m basket apples milk
Subtotal: £2.30
Apples 10% off: -10p
Total: £2.20
```
```
$ python -m basket milk soup eggs --verbose
2016-12-17 14:03:02 INFO: Item 'eggs' not in stock
Subtotal: £1.95
(No offers available)
Total: £1.95
```
```
$ python -m basket milk soup soup bread apples
Subtotal: £4.40
2 tins soup get you a half price loaf: -40p
Apples 10% off: -10p
Total: £3.90
```

## Tests
This application benefits from `pytest` tests. To run the tests:
```bash
$ pytest basket
``` 

## Environment
If you need to set up a working environment the following files can be used:

- `requirements.txt` - Classic pip requirements file.
- `environment.yml` - Conda environment definition file.
