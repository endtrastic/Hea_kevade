from modules_my import *
exit = False
i = 1
# Code looks like shit but if it aint broke, don't fix it.
def get_data():
    pag.hotkey('win', 'down')
    try:
        # Finds the link to "See more reviews" and clicks it
        all_reviews_site_link = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="reviews-medley-footer"]/div[2]/a')))
        all_reviews_site_link.click()
    except NoSuchElementException:
        pass
    except TimeoutException:
        pass
    except ElementClickInterceptedException:
        time.sleep(0.5)  

    time.sleep(7)
    # Checking if average score exists, to make sure that we are on the right page
    try:
        avg_score_on_product = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cm_cr-product_info"]/div/div[1]/div[2]/div/div/div[2]/div/span'))
        )
        print(f"Average rating on the product is: {avg_score_on_product.text}")
    # If it takes too long then we know that we arent on the right page and we exit out
    except TimeoutException: 
        print("Took too long there might not be any review ratings (Maybe)")
        keyboard.unhook_all()
        driver.quit()
        quit()
    time.sleep(1.5)
    # Checking if review count exists, to make sure that we are on the right page
    try:
        review_count = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="filter-info-section"]/div'))
        )
        print(f"Info on the products ratings and reviews: {review_count.text}", "\n")
    # If it takes too long then we know that we arent on the right page and we exit out
    except TimeoutException: 
        print("Took too long there might be no reviews :( (Maybe)")
        keyboard.unhook_all()
        driver.quit()
        quit()
    
    duplicate_remover()

def review_data():
    # Putting the data into a list to start removing duplicates from it
    reviews = []
    # Find the parent element where all the child elements that I want are stored in
    review_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "a-section.celwidget"))
    )
    # My ass is not coding that credit to: (CHATGPT)
    # Iterate through each review element and extract desired information
    for review_element in review_elements:
        try:
            # Extract reviewer name
            reviewer_name = review_element.find_element(By.CLASS_NAME, "a-profile-name").text

            # Extract review rating
            review_rating = review_element.find_element(By.CSS_SELECTOR, "i.a-icon-star").get_attribute("textContent")

            # Extract review title
            review_title = review_element.find_element(By.CLASS_NAME, "review-title-content").text

            # Extract review date
            review_date = review_element.find_element(By.CLASS_NAME, "review-date").text

            # Extract review comment
            review_body = review_element.find_element(By.CLASS_NAME, "review-text-content").text

            # Store the extracted information in dictionary
            reviewer = {
                'Reviewer Name': reviewer_name,
                'Review Rating': review_rating,
                'Review Title': review_title,
                'Review Date': review_date,
                'Review Body': review_body
            }
            reviews.append(reviewer)
        
        except NoSuchElementException:
            time.sleep(0.5)
        except socket.error:
            print("Connection error:")

    return reviews


def duplicate_remover():
    global i
    # Get the reviews from review_data()
    all_reviews = review_data()

# Remove duplicates based on Reviewer Name, Review Title, and Review Date
    unique_reviews = []
    review_identifiers = set()
    for review in all_reviews:
        identifier = (review['Reviewer Name'], review['Review Rating'], review['Review Title'], review['Review Date'], review['Review Body'])
        if identifier not in review_identifiers:
            unique_reviews.append(review)
            review_identifiers.add(identifier)

# Assign the data to a variable to make it easier to store into a database
    for data in unique_reviews:
        User = data['Reviewer Name']
        Title = data['Review Title']
        Rating = data['Review Rating']
        Comment = data['Review Body']
        date = data['Review Date']
# Inserting the info to the database
        print(data, "\n" * 2, f"Reviews found: {i}", "\n")
        c.execute('''INSERT INTO SCRAPED_INFO VALUES(?,?,?,?,?)''', (User, Title, Rating, Comment, date))
        conn.commit()
        i += 1

    next_page()

def next_page():
    global exit
    time.sleep(3.5)

    try:
        next_page_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cm_cr-pagination_bar"]/ul/li[2]/a'))
        )
    except TimeoutException:
        # If the next button isn't found, then the program prints out all the chosen info by the user in the database
        while exit != True:
            choice = input("Choose what you want to see from the database, User, Title, Rating, Comment or date   (Type quit to exit): ")
            if choice.lower() == "quit":
                # Could've used break, but my dumbass did not realise that
                exit = True
                keyboard.unhook_all()
                driver.quit()
                quit()
            else:
                try:
                    # Try to select it except when there's an error, then insult the user to get them to behave
                    c.execute(f'''SELECT {choice} FROM SCRAPED_INFO''')
                    data_in_database = c.fetchall()
                    print("\n", f"From the database selected: {choice} ", "\n")
                    print(data_in_database, "\n")
                except sqlite3.OperationalError:
                    random_insult_for_user = ["Are you a fucking dumbass?",
                                               "Oh you think ur funny, huh?",
                                                 "Stop acting like a child u dumbfuck",
                                                   "Did u hit your head and become a retard?",
                                                     "You can try, but I can do this shit all day long",
                                                      "I swear you do that one more time and i will find u and make you pay",
                                                       "Stop it",
                                                        "You ignorant piece of shit just cant contain yourself huh?" ]
                    print(random.choice(random_insult_for_user))

# Try to find the next button, if it exists click it
    try:
        if next_page_button:
            next_page_button.click()
            time.sleep(2)
            duplicate_remover()
    except UnboundLocalError:
        pass


get_data()

try:
    keyboard.wait("esc")
finally:
    keyboard.unhook_all()
    driver.quit()
