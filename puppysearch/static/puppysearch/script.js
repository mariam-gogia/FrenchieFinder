// keeping track of the current page in breeders reviews
let current_page_num = 1;
let current_breeder;
document.addEventListener('DOMContentLoaded', function() {

    // highlight the current page of the nav bar
    let current_url = document.location;
    document.querySelectorAll(".nav-item a").forEach(function(e) {
        if (e.href == current_url) {
            e.classList += " active";
        }
    });
    // container for reviews and breeder stats on breeders page
    document.querySelectorAll('.container_right').forEach(function(el) {
            el.style.display = 'none';
        })
        // when breeder is clicked
    document.querySelectorAll('.color_link_user').forEach(item => item.addEventListener('click', () => item_click(item.dataset.breeder, 1)))
    document.querySelectorAll('.favorite_btn').forEach(btn => btn.addEventListener('click', () => add_to_favorites(btn.dataset.listing)))

    if (document.querySelector('#submit_review') != null) {
        document.querySelector('#submit_review').addEventListener("click", add);
    }
    // pagination buttons for reviews
    btn_next = document.querySelector('#next_btn')
    btn_prev = document.querySelector('#prev_btn')
    if (btn_next != null) {
        btn_next.addEventListener('click', () => item_click(parseInt(current_breeder), current_page_num + 1))
        btn_prev.addEventListener('click', () => item_click(parseInt(current_breeder), current_page_num - 1))
    }
});

// add review 
function add() {
    fetch(`/add_review/${parseInt(current_breeder)}`, {
            method: 'POST',
            body: JSON.stringify({
                content: document.querySelector('#review-body').value,
            })
        })
        .then(response => response.json())
        .then(result => {
            item_click(current_breeder, 1)
            console.log(result)
        });
}

// add/remove listing from favorites
function add_to_favorites(listing_id) {
    btn_favorite = document.querySelector(`.favorite_btn[data-listing="${listing_id}"]`)
    fetch(`/add_to_favorites/${listing_id}/${btn_favorite.innerHTML}`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(result => {
            console.log(result)
            if (btn_favorite.innerHTML.trim() == "+ Favorite") {
                btn_favorite.innerHTML = '- Unfavorite';
                btn_favorite.id = "unfavorite_btn";
            } else {
                btn_favorite.innerHTML = '+ Favorite';
                btn_favorite.id = '';
            }
        });
}

// when breeder is clicked display the div containing stats, contact details and reviews
function item_click(breeder, page_num) {
    current_breeder = breeder;
    if (document.querySelector('#review-body') != null) {
        document.querySelector('#review-body').value = '';
    }
    document.querySelector('#reviews_view').innerHTML = '';
    document.querySelector('#review-form').style.display = 'block'
    document.querySelectorAll('.container_right').forEach(function(el) {
        el.style.display = 'block';
    })
    if (document.querySelector('#review-form').dataset.user == breeder) {
        document.querySelector('#review-form').style.display = 'none';
    }
    fetch(`/profile/${breeder}/${page_num}`)
        .then(response => {
            return response.json()
        })
        .then(data => {
            current_page_num = data.page_num

            document.querySelector("#company_label").innerHTML = data.breeder.company_name
                // populate HTML labels designated for contact details and stats
            let full_name = data.breeder.first_name + " " + data.breeder.last_name
            document.querySelector("#full_name").innerHTML = full_name
            document.querySelector("#member_since_label").innerHTML = data.breeder.timestamp
            document.querySelector("#count_label").innerHTML = data.num_active_listings
            document.querySelector("#sold_count_label").innerHTML = data.num_sold_listings
            document.querySelector("#email_label").innerHTML = data.breeder.email
            document.querySelector("#phone_label").innerHTML = data.breeder.phone
            document.querySelector("#active_listings_link").href = "/breeders_listings/" + data.breeder.id;
            // build the review div for each review 
            data.page_objects.forEach(review => {
                const reviewDiv = document.createElement('div');
                reviewDiv.className = 'reviews_inner_div';

                const reviewerlbl = document.createElement('LABEL');
                const timestamplbl = document.createElement('LABEL');
                const contnetlbl = document.createElement('P');

                reviewerlbl.innerHTML = review.reviewer.email;
                reviewerlbl.className = 'owner_label';
                timestamplbl.innerHTML = review.timestamp;
                timestamplbl.className = 'timestamp_label';
                contnetlbl.innerHTML = review.content;
                contnetlbl.className = 'review_content';

                reviewDiv.append(reviewerlbl);
                reviewDiv.append(timestamplbl);
                reviewDiv.append(contnetlbl);

                document.querySelector("#reviews_view").append(reviewDiv);
            })
            if (!data.page_has_next) {
                btn_next.style.display = 'none';
            } else {
                btn_next.style.display = 'block';
            }

            if (!data.page_has_previous) {
                btn_prev.style.display = 'none'
            } else {
                btn_prev.style.display = 'block'
            }
        })
}