# Frenchie Finder 


**Frenchie Finder** is a platform for breeders to post listings of their french bulldog puppies and for potential buyers to find the puppies they like. In recent years, breeders managed to develop rare colored frenchies, which dramatically increased the popularity of this dog breed worldwide. Unfortunately, there was no platform that enabled potential buyers to look for the frenchies they wanted. As someone who has spent 7 months looking for a french bulldog puppie all over the internet, I decided to create this web app to help other potential buyers like me find the puppies they like and offer breeders a platform to showcase their puppies. 

The website is currently only focused on the US market. 

## Functionalities 

### Registration
The platform allows 2 types of users: **breeders** and **seekers.** Upon registration the user must select which type of user he/she is. If user registers as a breeder he/she will have additional privileges such as 'Add Listing' and 'My Listings.' Breeder will also be able to see his/her reviews that others have given to him/her.

## Home 
### Seach Bar 
Home page (index) contains a search bar. Search bar allows users to look for puppies using their:
- Color
- Location
- Breeder
- Listing ID
- Puppy's name

### Listings
Listings are displayed in reverse chronological order. The page utlizies pagination and only displayes 10 listings per page. Each listing contains the following information:

- A button to add/remove a puppy from user's favorites list
- Puppy's name and listing ID
- Color *(clickable)*
- Description
- Breeder *(clickable)*
- Location *(clickable)*
- Date posted

If the listing belongs to the logged in user, instead of 'Favorite/Unfavorite' button the user will see 'Actions' drop-down which will allow the user to:

- Delete listing
- Mark as Sold

## Colors
Colors page displayes potential colored frenchies available along with an example picture of them. The picture is there to let users know what a frenchie marketed with given color should look like. 
Clicking on the color takes the user to all the available listings in that color category. For exaple, if user clicks on **Lilac**, he/she will be shown all the available **Lilac** puppies. 

## Breeders
### Breeders List
Breeders page first displays the list of breeders *(clickable)*. Breeders are displayed by their company name and by alphabetical order. 

### Breeder's Profile
Once the user clicks on breeder, new section pops up on the right hand side. The section contains:

- Contact information of the breeder
- Statistics including the clickable 'Active Listings' link
- Reviews: 
		- If the logged-in user is not a breeder himself, the user can add a review to another breeder.
		- Reviews section utilizes pagination, only 3 reviews are displayed per page. 'Next' and 'Prev' buttons appear if the breeder has more than 3 reviews. 
		- The body of the review itself is scrollable. 

## Locations
Locations page displays all the locations where puppies may be available. When breeder signs up, he/she is required to provide location information. Location provided is then added to the locations list as it becomes a possible location where a seeker may find the puppie. Clicking on the specific location takes user to all the listings available in that location.

## Add Listing
Only the breeders are allowed to add a listing. The page displays a form where a breeder is required to provide:

- Puppy's name
- Description
- Price
- Image URL
- Pick a color
- Pick a location

## User's Profile
User's username is displayed at the end of the navigation bar. Clicking it will cause a drop-down menu to pop up. If the signed in user is a breeder he/she will have following choices:

- Favorites: showing all the listings that the user favorited
- My Listings: showing all the listings a breeder has created
- My reviews: Left hand-side showing all the recieved reviews, the right hand-side showing all the given reviews
- Log out

Non-breeder user will also see the similar drop-down, however, he/she will not have 'My Listings' section and in 'My Reviews' he/she will only see the reviews given.



## Files & Details

The project has followed the typical project directory design we have been exercising throughout the whole semester. It has two folders 'puppysearch' and 'finalproject'

All the HTML templates are placed in *puppysearch/templates/puppysearch*

Static folder contains the media folder which has all the pictures inside. Static folder also contains the script.js and styles.css files, both of which were heavily used in this project. 

Project uses 5 models all of which are placed in puppysearch/models.py 

superadmin credentials: admin admin

Code style has been checked using

pycodestyle --max-line-length=120

There are 4 lines that do not fulfill <120 character requirements: In *puppysearch/views.py* in 'search' function querying models resulted in longer lines than 120 characters, however, it was left untouched deliberetely as an author considered it more readable that way.

### Other Comments
The author originally wanted to create a marketplace type of platform for puppies but later realized that people do not buy puppies online, so more useful use-case would be to create a platform where people could search for puppies and contact breeders. The author also realized that it would have been better to have a niche and focus on one breed rather than have all breeds available. Only above described changes were made to the original proposal and the author believes she met the 'Best Outcome' for her project. 

