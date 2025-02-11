## Django OnAuc: Online Auction Platform

### Overview
OnAuc is a Django-based online auction platform that offers a robust user experience with features such as user authentication, auction creation, bidding, and real-time chat.
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/auction-page.png)

### Core Features

#### User Authentication and Management
* Django All Auth: Handles user registration, login, logout, password reset, and social authentication.
* Custom User Model: Extends Django's built-in User model with additional fields like contact information, preferred auction types, etc.

#### Auction Creation and Management
* Auction Types:
  * Public: Visible to all registered users.
  * Private: Visible only to the creator and invited users.
  * Contacts Only: Visible only to the creator's contacts.
* Auction Creation: Users can create auctions with detailed descriptions, starting bids, end times, and auction type.
* Private Links: Users can generate private links for private and contacts-only auctions to share with specific individuals.
* Auction Dashboard: Users can manage their created and watched auctions.
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/auciton-create.png)
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/auction-additional-feilds.png)
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/auction-contacts.png)
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/add-private-links.png)
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/private-link-settings.png)
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/auction-dashboard.png)
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/auction-detail-dashboard.png)

#### Bidding and Auction Progress
* Bidding System: Real-time bidding with bidding history and highest bidder information.
* Auction Timer: Countdown timer for each auction.
* Auction Ending: Automatic auction closure and notification to the winner.
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/auction-bid.png)

#### User Interaction and Communication
* Chat Functionality: Real-time chat within each auction for bidders to communicate.
* User Profiles: Basic user profiles with contact information and auction history.
* Saved Auctions: Users can save auctions for later viewing.
* User Contacts: Users can manage their contact list.
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/auction-chat.png)
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/auction-contacts.png)
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/auction-cart.png)

#### Payment and Card Management
* Card Saving: Users can save credit card information for faster checkout (without requiring login).
* Secure Card Storage: Encrypted card data stored securely in the database after login.
* Payment Integration: Integration with payment gateways for auction purchases.
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/auciton-order.png)

#### Additional Features
* Admin Roles: Users can assign admin roles to other users for their auctions.
* Customizable Auction Fields: Flexible auction creation with additional custom fields.
* Search and Filtering: Advanced search and filter options for auctions.
* Notifications: Email and in-app notifications for auction updates, bids, and messages.
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/add-admins-to-auction.png)
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/edit-admins-permissions.png)
![Auctions Page](https://github.com/bahromnajmiddinov/media-files/blob/main/auction-media/auction-profile.png)

### Technical Implementation
* Django Framework: Core web development framework.
* Django Rest Framework: API for mobile app or other integrations.
* Database: (not implemented) PostgreSQL for storing user data, auctions, bids, and other information.
* Frontend: HTML, CSS, JavaScript, and a frontend framework like React or Vue for a modern user interface.
* Real-time Communication: WebSocket for real-time communication for chat and bidding updates.
* Payment Gateway Integration: Stripe, PayPal, or other payment providers.
* Security: Robust security measures to protect user data and prevent fraud.

### Future Enhancements
* Mobile App: Develop a mobile app for better user experience.
* Auction Categories: Introduce auction categories for better organization.
* Image and Video Uploads: Allow users to upload images and videos for auction items.
* Feedback and Ratings: Implement a rating system for buyers and sellers.
* Auction Bidding History: Detailed bidding history for each auction.
