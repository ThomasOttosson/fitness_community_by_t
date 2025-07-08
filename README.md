# FitCommunity: Achieve Your Health Goals

[![Project Status](https://img.shields.io/badge/Status-Complete-brightgreen)](https://github.com/ThomasOttosson/fitness_community_by_t)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Project Overview

This project is a full-stack e-commerce application for a fitness business, designed to help users achieve their health and wellness goals. Built as part of the Diploma in Full Stack Software Development (E-commerce Applications), it offers personalized exercise plans, nutrition guidance, and high-quality fitness products. Users can browse content, make one-time purchases, subscribe to recurring plans, and manage their account and subscriptions seamlessly.

## Features

### Navigation & User Access

Responsive Header & Navigation: A clean, responsive header with a light background, subtle shadow, and dynamic navigation links. It includes:

* "Fitness Site" logo link to the Home page.
* Direct links to Exercise Plans, Nutrition Plans, and Products lists.
* Mobile Offcanvas Menu:** For small screens, a slide-out menu provides an intuitive navigation experience.
* Dynamic User Menu:** If logged in, a dropdown menu replaces login/register, providing quick access to:

* Profile, Cart, Order History.
* Subscriber Dashboard:** For active subscribers to access exclusive content.
* Staff Dashboard:** For site administrators to manage users.
* Django Admin backend link (for staff).
* Logout option.
User Authentication & Authorization:
* Secure user registration, login, and logout with custom-styled, Bootstrap 5 floating forms for a premium feel.

Role-Based Access Control:

* Django Admin backend accessible only to `is_staff` users (administrators/owners).
* Dedicated Staff Dashboard (front-end) displaying a dynamic list of all users, their subscription status (Paying/Not Subscribing), and roles (Staff/Admin/Active/Inactive), accessible only by `is_staff` users.
* Protected content pages for Exercise and Nutrition Plans, accessible only by users with an active subscription to that specific plan type. The menu updates with the specific user logged in.

### Content & Catalog

- Hero Section: A powerful visual with bold text, "NOW THERE'S NO EXCUSE. GET FIT ON SITE.", accompanied by "GET STARTED" and "MY ACCOUNT" call-to-action buttons.

- "Put Your Health First" Section: Highlights the importance of health with compelling text and a relevant image of someone measuring their waist, encouraging users to begin their journey.

- Our Top Products Section: Showcases products in consistent cards with images, names, prices, star ratings, and "VIEW DETAILS" buttons. A "VIEW ALL PRODUCTS" button leads to the full catalog.

- Exercise Plans Section: Displays various workout routines in card format, including images, plan names, prices, and star ratings, with a "VIEW DETAILS" button and "VIEW ALL EXERCISE PLANS" option. Similarly Nutrition Plans Section: Presents balanced meal guides similarly in cards, featuring images, plan names, prices, and star ratings, alongside "VIEW DETAILS" and "VIEW ALL NUTRITION PLANS" buttons.

- "Make Your Gym Anywhere" Section: Emphasizes workout flexibility with a strong title, descriptive text, and an image of home exercise, including a "GET STARTED" button.

- Subscribe Today Section: A yellow section prompting sign-ups for guided training via email, username, and password fields, finalized by a "GET STARTED" button.

- What Our Clients Say Section: A testimonial carousel showcasing positive feedback from satisfied clients, building trust through their success stories.

- "Get In Touch" Section: Provides clear contact information—address, phone, and email—each accompanied by a distinct icon for easy readability.

- Footer: Contains the brand logo and mission, quick navigation links (Home, Plans, Products, Profile), a newsletter sign-up, and social media connection icons.
  
* Browseable Lists: Each product type has its own dedicate page as discussed below:
* Exercise plan page: 

This page, titled "Our Exercise Plans", showcases various workout subscriptions offered by Fit Community.
At the top, the Fit Community logo is visible along with navigation links for Home, Exercise Plans, Nutrition Plans, Products, and a user profile dropdown.
The main content displays individual exercise plans, each presented in a clean card format.
Each plan card features a relevant image, a descriptive title, a short overview, a star rating with review count, the price, and a "VIEW DETAILS" button.

Our Nutrition Plans Page:

* This page, titled "Our Nutrition Plans," displays various diet and meal planning subscriptions.
The top includes the Fit Community logo and navigation links.
Each nutrition plan is presented in a card format, showing a relevant image, plan title, a short description, star rating, and price.
Users can click "VIEW DETAILS" on each card to learn more about the specific plan.

* Our Fitness Products Page This page, titled "Our Fitness Products," showcases the merchandise available from Fit Community.
* The top features the Fit Community logo and standard navigation options.
Products are displayed in individual cards, each with an image, product name, a brief description, star rating, and price.
* A "VIEW DETAILS" button on each card allows users to access more information about the product.

Detailed view for the Subscription and product pages:

Detailed Views: Individual pages for Exercise Plan:
This page provides detailed information for a specific exercise plan. It features a large image relevant to the plan, the plan's title, price, and duration. A comprehensive description outlines the workout routine's benefits and features. Purchase options include "SUBSCRIBE NOW" and "ADD TO CART (ONE-TIME)," with an adjustable quantity. Below, existing customer reviews are shown, and a form allows authenticated users to submit new ratings and comments. The page concludes with the standard site footer.

Nutrition Plan Detailed View Page:
This page provides a detailed view of a specific nutrition plan, featuring a large image, the plan's title, price, and duration. A comprehensive description outlines the plan's benefits. Purchase options include "SUBSCRIBE NOW" and "ADD TO CART (ONE-TIME)," with a quantity selector. Below, "Customer Reviews" are displayed, and an input form allows authenticated users to submit new ratings and comments. The standard site footer is present at the bottom.

Product Detailed View Page:
This page presents a specific product in detail, featuring a large image of the item (like gym gloves), its title, and price. A comprehensive description highlights the product's features and benefits, along with availability information. Users can select a quantity and "ADD TO CART." Below, customer reviews are displayed, and an input form allows authenticated users to submit their own ratings and comments. The standard site header and footer are also present.

Profile Page:

This is a personalized dashboard for logged-in users, displaying a "Welcome, [Username]!" message. It's divided into "Account Details," showing the username, email, and join date. "Account Actions" provides links to order history, subscriber dashboard, staff dashboard (if applicable), and an "Edit Profile" option. Below, "Your Active Subscriptions" shows current plans or prompts to browse for new ones. A "LOGOUT" button is prominently displayed for ending the session.

### E-commerce & Payments

Shopping Cart:

This page functions as the user's persistent shopping cart, where various items can be managed. Users can add products, exercise plans, and nutrition plans, which remain in the cart across sessions. On this page, quantities can be adjusted and items removed, with the total cost updating in real-time. Adding an item to the cart seamlessly redirects the user here with a clear confirmation.

Checkout Process:

This secure page displays the order summary, facilitating payment for items in the cart. One-time product purchases use Stripe Payment Intents for secure card collection directly on the page. Subscription purchases for plans redirect users to Stripe Checkout Sessions for optimized recurring payments. The system robustly handles payment outcomes (success, pending, failure) with clear messages and redirects to prevent duplicate notifications.

Subscriber Dashboard Page:

This page serves as a personalized hub for subscribers, welcoming them and offering access to exclusive content. It clearly lists "Your Active Subscriptions," detailing each plan (e.g., Nutrition, Exercise) along with its activation date. A prominent "MANAGE MY SUBSCRIPTIONS (STRIPE PORTAL)" button allows users to handle their subscriptions directly via Stripe.

Order & Subscription History:

This page displays a comprehensive list of all past orders made by the user. Each order is presented in a collapsible panel, showing the order number, date, and total amount. Expanding an order reveals detailed information, including individual items purchased and the payment intent ID. A "CONTINUE SHOPPING" button is available at the bottom to redirect the user back to browse products and plans.

Protected pages for staff & subscribers:

* Staff Dashboard page:

This "Staff Dashboard" serves as a comprehensive administrative control center. At the top, a "Last updated" timestamp indicates the most recent data refresh. Key performance metrics are prominently displayed in distinct cards: "Total Users," "Active Subscribers," "Staff Members," and "Active Users," each with an icon and count.
An "Administrative Control" section provides quick access to advanced system management and configuration tools via a "DJANGO ADMIN" button. The primary "User Management" section features a search bar for users, and filters to display "ALL USERS," "SUBSCRIBERS," or "STAFF." This section also includes "EXPORT" and "REFRESH" buttons for data handling.
The user table presents detailed information including username, contact details (email or last login), subscription status (e.g., Free), and assigned "STATUS & ROLES" such as "Active," "Staff," and "Admin." The "JOINED" column shows the registration date for each user. Finally, a "BACK TO PROFILE" button allows staff to return to their personal profile page. The standard site header and footer are present. In case the user is not an active subscriber, they will see this notification: "Active subscription required."

Subscribers only pages:

* Monthly Nutrition Plan Subscription Page:

This exclusive content page is accessible only to users with an active subscription to the "Monthly Nutrition Plan Subscription, Standard or other subscriptions based on which the page content will be updated." It features a prominent title and a congratulatory message confirming the active subscription. An accompanying image highlights the nutrition plan. The page then lists "Your Nutrition Guidelines," which include detailed meal plans, a personalized hydration guide, a printable grocery list, healthy recipe ideas, and exclusive nutrition tips. A clear note states that this content is visible only to subscribers of this specific plan. A "BACK TO DASHBOARD" button allows users to return to their subscriber overview.

Monthly Exercise Plan Subscription Page:

This exclusive page provides content visible only to users with an active subscription to this specific exercise plan. It features a congratulatory message and an image illustrating a workout schedule. The page lists "Your Exercise Routines," including warm-ups, detailed full-body, upper-body, and lower-body workouts, cool-downs, and a weekly training schedule. A "BACK TO DASHBOARD" button allows subscribers to return to their overview.

Stripe Customer Portal Page:

Accessible from the "Subscriber Dashboard," this external portal, hosted by Stripe, allows users to manage their billing and subscriptions directly via Stripe. It displays the user's "PAYMENT METHOD," including default cards and an option to "Add payment method." "BILLING INFORMATION" shows details like name, address, and phone number, with an option to "Update information." Users can also view their "INVOICE HISTORY" here, simplifying billing management. The page emphasizes its partnership with Stripe for secure and simplified billing. On test mode it only works with verified emails.

### Marketing & SEO

* Mailchimp Newsletter Integration:

* Newsletter signup form in the site footer, directly integrated with Mailchimp API.
* User-friendly feedback for successful subscriptions and a custom message for existing subscribers.

Search Engine Optimization (SEO):
* Robots.txt: Configured to guide search engine crawlers.
* Sitemap.xml: Dynamically generated sitemap to help search engines discover all public pages (home, lists, detail pages).
* Meta Tags: Dynamic `<title>` and `<meta name="description">` tags for each major page, optimized for search engine results.
* Custom 404 Page: Provides a user-friendly experience and proper HTTP status for non-existent URLs.

404 page:

This page is displayed when a requested URL cannot be found. It prominently shows a large "404" error code and "Page Not Found" message. A concise explanation states the page might be missing or the link is broken. Users are offered a clear "Go to Homepage" button to navigate back to the main site. A small message suggests contacting support if the error persists. The standard site header and footer are visible on this page.

### User Experience Design (UI/UX)

* Commercial-Grade Design: The site boasts a clean, modern, and professional aesthetic, consistently applied across all pages.
* Custom Branding: Incorporates a defined color palette and typography (Headings: Montserrat, Body: Open Sans) for a cohesive brand identity.
* Custom Buttons: Unique, clipped-path button styling with gradient backgrounds for interactive elements.
* Responsive Layout: Fully adaptive design using Bootstrap 5's grid system, ensuring optimal viewing and functionality across desktops, tablets, and mobile devices.
* Intuitive Interactions: Clear navigation paths, prominent calls-to-action, and user-friendly forms.

## Technologies Used

Backend:

* Python 3.13
* Django 5.2.3 (Web Framework)
* PostgreSQL (Relational Database)
* `dj_database_url` (For seamless database connection in production)

Frontend:

* HTML5 (Structure)
* CSS3 (Custom Stylesheets)
* Bootstrap 5 (CSS Framework & Components)
* JavaScript (Custom logic & Bootstrap JS Bundle)
* Font Awesome (Vector Icons)

Third-Party Integrations (APIs):
* Stripe (For Payment Processing: Payment Intents, Checkout Sessions, Customer Portal)
* Mailchimp (For Email Newsletter Management)

## Setup and Installation

Follow these steps to get the Fitness Site running on your local machine:

1.  Clone the repository:

    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd fitness-site
    ```
    (Replace `yourusername/your-repo-name.git` with your actual GitHub repository URL).

2.  Create and activate a virtual environment:

    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  Install dependencies:

    First, ensure you have a `requirements.txt` file (create it if not present by running `pip freeze > requirements.txt` after installing initial dependencies).
    Then install all requirements:
    ```bash
    pip install -r requirements.txt
    ```

4.  Set up environment variables:

    Create an `env.py` file in the root of your project (next to `manage.py`) and add the following Python variables, replacing placeholders with your actual secrets and configurations. **DO NOT commit this `env.py` file to your Git repository.**

    ```python
    # env.py
    os.environ.setdefault('SECRET_KEY', 'your-secret-key-here')

    # Database Credentials /link
    os.environ.setdefault(
    'DATABASE_URL',
    'your-db-url',)

    # Stripe API Keys (from your Stripe Dashboard - use test keys for development)

    os.environ.setdefault(
        'STRIPE_PUBLISHABLE_KEY',
        'test-or-real-key-here',
    )
    os.environ.setdefault(
        'STRIPE_SECRET_KEY',
        'test-or-real-key-here',
    )

    # Mailchimp API Credentials (from your Mailchimp Account)
    os.environ.setdefault(
        'MAILCHIMP_API_KEY',
        'keyhere-prefix',
    )
    os.environ.setdefault('MAILCHIMP_AUDIENCE_ID', 'real-id-here')
    os.environ.setdefault('MAILCHIMP_SERVER_PREFIX', 'prefix-key')
    ```

    * **Generate a strong `SECRET_KEY`**: Run `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` in your terminal.
    * **Update `.gitignore`**: Ensure `env.py` is listed in your `.gitignore` file to prevent accidental commits.

5.  Apply Database Migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  Create a Superuser (for Django Admin access):

    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts.

7.  Run the development server:

    ```bash
    python manage.py runserver
    ```
    The application will be accessible at `http://127.0.0.1:8000/`.

8.  Upload Sample Data:

    Access the Django Admin (`http://127.0.0.1:8000/admin/`) with your superuser account. Add some `ExercisePlan`, `NutritionPlan`, and `Product` instances, ensuring you upload images. Set the `stripe_price_id` for subscription items (obtained from your Stripe Dashboard) for recurring plans. Add a few test reviews to items.

## Third-Party Service Configuration

For full functionality, configure these services:

Stripe Dashboard:

* Products & Prices:
    
Create `Products` in Stripe that correspond to your Django `ExercisePlan`, `NutritionPlan`, and `Product` models. For subscription items, create **Recurring Prices** (e.g., "$10/month") and note down their `price_ID` (`price_123xyz...`). Update your Django Admin entries for `ExercisePlan` and `NutritionPlan` models with these `price_ID`s.

* Customer Portal:

Go to Settings -> Customer Portal in your Stripe Dashboard. Configure its features (what users can do). Activate the direct login URL** and paste this URL into your `templates/registration/profile.html` and `templates/registration/subscribed_dashboard.html` files.

* API Keys: 

Ensure your `STRIPE_PUBLISHABLE_KEY` and `STRIPE_SECRET_KEY` in `env.py` (or production environment variables) match your Stripe Dashboard test API keys (for development).

*   (Optional but recommended for robust subscription management): Set up Stripe Webhooks to listen for events like `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_succeeded`, etc.

* Mailchimp Account:

*   Create an **Audience** (List) for your newsletter subscribers.
*   Note down your Audience ID, API Key, and Server Prefix from your Mailchimp account details. Update these in your `env.py` file.

Font Awesome:

* Sign up for a free Font Awesome account at [fontawesome.com](https://fontawesome.com/).
* Create a "Kit" and get your unique script tag (e.g., `<script src="https://kit.fontawesome.com/YOUR-KIT-CODE.js" crossorigin="anonymous"></script>`).
* Paste this script tag into your `templates/base.html` within the `<head>` section.

## Testing Guidelines

Perform comprehensive testing to ensure all features work as expected:

* User Authentication: Register a new user, log in, log out. Verify correct display of Profile page, Subscriber Dashboard, and Order History.

* Product/Plan Browsing: Navigate through Home, Exercise Plans, Nutrition Plans, and Products list pages. Click on individual items to view their detail pages.

* Cart & Checkout:

Add various products and plans to the cart. Update quantities and remove items. Proceed to checkout and complete successful test payments (one-time & subscription via [Stripe test card numbers](https://stripe.com/docs/testing#cards)). Verify orders and subscriptions appear correctly in the Django Admin.

* Subscription Management: Access the Stripe Customer Portal from your Profile/Dashboard and verify its functionality.

* Reviews:
Submit reviews (rating and comment) on detail pages for products/plans. Verify review display on the detail page and average ratings on listing/homepage sections.

* Newsletter:
Submit email via the footer form. Verify the email appears in your Mailchimp Audience. Test with an already-subscribed email to see the custom warning message.

* Role-Based Access: 

Log in as a staff user (e.g., your superuser). Access the Staff Dashboard (`/staff-dashboard/`). Verify its content. Log in as a non-staff user. Attempt to access `/staff-dashboard/` directly (should be denied). Verify subscription content protection: access content for subscribed plans vs. non-subscribed plans.

* Responsiveness: Test all major pages on various screen sizes (using browser developer tools) to ensure layout adapts correctly, especially the header's offcanvas menu.

* Error Handling & SEO: Temporarily set `DEBUG = False` in `env.py` and restart the server. Navigate to a non-existent URL (e.g., `http://127.0.0.1:8000/this-page-does-not-exist/`) to verify the custom 404 page is displayed. Verify `http://127.0.0.1:8000/robots.txt` and `http://127.0.0.1:8000/sitemap.xml` are accessible. View page source on key pages to confirm correct meta titles and descriptions.


### Manual Testing

| Action / Test Case                                         | Expectation                                                                                | Pass/Fail |
| :--------------------------------------------------------- | :----------------------------------------------------------------------------------------- | :-------- |
| **Authentication & Profile**                               |                                                                                            |           |
| Register a new user                                        | User can fill out the styled registration form (username, email, password, confirm password) following password rules and successfully create an account. Confirmation message displays. | Pass      |
| Log in with valid credentials                              | User is successfully authenticated and redirected to their Profile page. | Pass      |
| Log in with invalid credentials                            | User receives an error message, remains on login page.                                     | Pass      |
| Log out                                                    | User is logged out and redirected to the homepage/logout confirmation.                       | Pass      |
| Access Profile page                | Displays user details, account actions, and a list of active subscriptions. Links work.      | Pass      |
| Access Order History page            | Displays a list of past one-time purchases in an accordion layout. Empty state handled.      | Pass      |
| Access Subscriber Dashboard                 | If subscribed: Displays active subscriptions with links to content. If not subscribed: Displays a message prompting subscription. | Pass      |
| Access Staff Dashboard                | If `is_staff=True`: Displays user statistics table with subscriber/role status. If `is_staff=False`: Redirects to home with an error. | Pass      |
| **Content Browsing & Detail Pages**                        |                                                                                            |           |
| Navigate from Home to list pages                           | Links to Exercise Plans, Nutrition Plans, and Products lists work correctly.                 | Pass      |
| View Exercise Plan / Nutrition Plan / Product list         | Items display in a consistent card layout with images, prices, average ratings, and review counts. | Pass      |
| Click item on list page to view detail                     | User is forwarded to the detailed page for that specific item.                             | Pass      |
| View any detail page (Product, Exercise Plan, Nutrition Plan) | Displays comprehensive info, image, price, description, average rating, and all submitted reviews. | Pass      |
| Access Protected Content | If subscribed: Displays exclusive content for that plan. If not subscribed: Redirects to plan detail/home with an error. | Pass      |
| **Cart & Checkout**                                        |                                                                                            |           |
| Add item to cart from detail page (with quantity)          | Item (with specified quantity) is added to cart, and user is redirected to cart page. Single success message displayed. | Pass      |
| Add item to cart from list page (default quantity 1)       | Item is added to cart (quantity 1), and user is redirected to cart page. Single success message displayed. | Pass      |
| View Cart page                                  | Displays correct cart contents, quantities, individual totals, and grand total. Empty state handled. | Pass      |
| Update item quantity in cart                               | Quantity updates, line item total, and cart total are recalculated correctly. Single success message. | Pass      |
| Remove item from cart                                      | Item is removed from cart, cart total updates. Single success message.                     | Pass      |
| Proceed to Checkout                                        | User is forwarded to the checkout page, displaying order summary and Stripe payment form.    | Pass      |
| Complete successful Stripe test payment (one-time product) | Payment processes successfully, user is redirected to Payment Successful page. Single success message. Order is created in Django Admin. | Pass      |
| Complete successful Stripe test payment (subscription)     | Subscription activates, user is redirected to Payment Successful page. Single success message. Subscription record created in Django Admin. | Pass      |
| Simulate Stripe payment failure / cancellation             | User is redirected to Payment Failed page with appropriate error message.                   | Pass      |
| Refresh Payment Successful/Failed page                     | Messages do NOT reappear on page refresh due to PRG pattern.                               | Pass      |
| **User Engagement & Marketing**                            |                                                                                            |           |
| Submit a review on a detail page                           | Review (rating + comment) is successfully submitted, displayed, and stored in DB. Confirmation message. | Pass      |
| Submit newsletter signup (new email)                       | Email is added to Mailchimp audience. Success message displayed.                           | Pass      |
| Submit newsletter signup (existing email)                  | User receives a friendly "already subscribed" message.                                     | Pass      |
| Access Stripe Customer Portal from Profile/Dashboard       | User is redirected to Stripe's hosted portal for self-management of subscriptions.         | Pass      |
| **General UI/UX & Responsiveness**                         |                                                                                            |           |
| Header & Footer display                                    | Appear consistently on all pages with correct branding, fonts, and colors.                 | Pass      |
| Header Mobile Offcanvas Menu                               | On mobile: toggler opens a functional offcanvas menu. On desktop: offcanvas hidden, standard menu visible. | Pass      |
| Custom Button Styles                                       | All custom buttons (Subscribe, Add to Cart, etc.) display the unique clipped path and gradient effect. | Pass      |
| Form Field Styling                                         | Login & Register inputs display rounded borders, transparent backgrounds, and floating labels correctly. | Pass      |
| Navigation across site                                     | All internal links correctly navigate to the expected pages.                               | Pass      |
| Site responsiveness on various devices                     | Layouts adapt gracefully to different screen sizes (mobile, tablet, desktop).              | Pass      |
| **Error Handling & SEO**                                   |                                                                                            |           |
| Access non-existent URL (`DEBUG=False` in `env.py`)        | Custom 404 "Page Not Found" template is displayed.                                         | Pass      |
| Access `robots.txt`                                        | Correct `robots.txt` file content is displayed.                                            | Pass      |
| Access `sitemap.xml`                                       | Valid XML sitemap is generated and displayed, listing all relevant URLs.                   | Pass      |
| View Page Source for meta tags                             | `<title>` and `<meta name="description">` tags are correct and specific to each page.      | Pass      |

### Code Validation (More Testing)

*   **PEP8 Python Style:** Adherence to Python Enhancement Proposal 8 (PEP8) for code style.
    *   Validation Tool: [https://pep8ci.herokuapp.com/](https://pep8ci.herokuapp.com/)
*   **CSS Validation:** Checks for valid CSS syntax and properties.
    *   Validation Tool: [https://jigsaw.w3.org/css-validator/#validate_by_input](https://jigsaw.w3.org/css-validator/#validate_by_input)
*   **HTML Validation:** Checks for valid HTML5 syntax and structure.
    *   Validation Tool: [https://validator.w3.org/nu/](https://validator.w3.org/nu/)
*   **JavaScript Linting:** Identifies potential errors, problematic patterns, and style issues in JavaScript.
    *   Validation Tool: [https://jshint.com/](https://jshint.com/)

## Project Story

My inspiration for creating this project stemmed directly from the Code Institute's Full Stack Software Development program, particularly the modules on Django and e-commerce applications. As someone passionate about fitness, health, and personalized wellness journeys, I envisioned building a platform that not only offered valuable resources but also provided a seamless and premium user experience. I wanted to move beyond a static content site and create a dynamic e-commerce solution where users could truly invest in their health through structured plans and quality products.

I began the design process by creating a wireframe for the homepage to visualize the user flow and overall aesthetic. My goal was to create a custom, commercial-grade design that felt consistent and premium, applying a specific color palette, custom fonts, and unique button styles throughout the site. This focus on UI/UX was central to the project's success. Before starting the design of the website, I chose the colors and fonts. The logo I designed was created using assets from two sources: https://www.svgrepo.com/ and https://www.canva.com/. The icon was sourced from Svgrepo, and the logo's design was completed in Canva.

Throughout the development, I embraced the challenge of integrating complex real-world functionalities. Implementing **Stripe for both one-time product purchases and recurring subscriptions** was a significant learning curve, requiring meticulous backend logic for payment intents, checkout sessions, and post-payment order/subscription fulfillment. Managing user data and access through robust **role-based authorization** (distinguishing between general users, subscribers, and staff administrators) further deepened my understanding of secure web applications. Integrating **Mailchimp for newsletter management** and perfecting the **responsive design with Bootstrap 5's intricacies** were also rewarding aspects of this project. Ultimately, overcoming these challenges allowed me to apply my knowledge, explore new tools, and deliver a fully functional, highly polished e-commerce platform.

## Deployment

This application is configured for deployment to a cloud hosting platform (e.g., Heroku, Render). Key production-ready configurations are integrated:

*   `dj_database_url` used for PostgreSQL connection strings (e.g., via a `DATABASE_URL` environment variable).
*   `ALLOWED_HOSTS` configured for production domains (must set `ALLOWED_HOSTS` environment variable on hosting platform).
*   `DEBUG=False` (must be explicitly set `False` in production environment variables).
*   Secure `SECRET_KEY` loading from environment variables.
*   `STATIC_ROOT` and `MEDIA_ROOT` configured for static file collection (`python manage.py collectstatic`) and serving by the production web server (e.g., Nginx, or `WhiteNoise` for simpler setups).
*   A `Procfile` (if deploying to Heroku/Render) defines the `gunicorn` web process.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. A copy of the license is available in the `LICENSE.md` file.