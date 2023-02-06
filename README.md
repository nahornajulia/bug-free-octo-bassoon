# SpeedBird Cafe ordering test 

## Summary

## How to launch
You can use a small automated bash script
to prepare environment and launch the demo tests
`./prepare.sh`
And to clean up the stuff launch 
`./prepare.sh clean`

## Notes
### Directory structure
The test itself is quite small, to split it by files 
and put them into different directories. 
But it shouldn't be hard to adjust it to some existing project layout

## Suggestions
### '>>2.' Additional scenarios you can imagine.
- test functionality on different environments(Chrome, Safari)
- include paging (test to include other pages of products etc.)
- check if there are all needed attributes(Price, Name, Picture, Avios) on each product
- check if click on the product -> there will be an additional info window

### '>>3.'Can you figure out any edge case scenario?
- test what if there are no products in the list
- check order of product list on the next pages
- check that there are 9 products per page

### '>>4.' Would you suggest some unit or integration test to the developers team?
#### Integration test cases:
- Check that if click Add to bag -> product is in the Сart
- Check that if to add several products to the bag -> Price of the products in the Cart is correct
- Check that to add product to the wish list -> user needs to be logged in to the site
- Check if add 5 times same product to the bag -> there are 5 products in the Cart list
#### Unit test cases:
- (FrontEnd) check if sorting supports localization -> there is correct sorting by given field
- (BackEnd) server returns some particular amount a data per each page
