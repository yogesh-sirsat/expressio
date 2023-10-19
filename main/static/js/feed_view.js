$(document).ready(async function () {
    let globaL_posts_page = 1;
    let following_authors_posts_page = 1;
    let isLoading = false;  // Prevent multiple requests while loading

    function hasReachedBottom() {
        let windowHeight = $(window).height();
        let documentHeight = $(document).height();
        let scrollTop = $(window).scrollTop();

        return (windowHeight + scrollTop) >= (documentHeight - 800);
     }
    async function loadMorePosts(posts_type) {
        
        if (!isLoading) {
            isLoading = true;
            if (posts_type === "global") {
                $('#global-posts-bottom').html("Getting Posts...");
            } else {
                $('#following-authors-posts-bottom').html("Getting Posts...");
            }
            await $.ajax({
                url: '/get_paginated_posts',
                type: 'GET',
                data: {
                    page: posts_type === "global" ? globaL_posts_page : following_authors_posts_page,
                    posts_type: posts_type,
                },
                success: function(data) {
                    if (data.rendered_posts) {
                        if (posts_type === "global") {
                            $('#global-posts article').append(data.rendered_posts);
                            globaL_posts_page++;
                        } else {
                            $('#following-authors-posts article').append(data.rendered_posts);
                            following_authors_posts_page++;
                        }
                    } 
                    if (!data.has_next_page) {
                        if (posts_type === "global") {
                            $('#global-posts-bottom').html("Yepp, you catched up all posts!");
                        } else {
                            $('#following-authors-posts-bottom').html("Yepp, you catched up all posts of following authors!");
                        }
                    }
                    //redirect to post view when click on post title | thumbnail
                    $(".post_item .card-img-top, .post_item .card-title").on('click', function() {
                        window.location = $(this).parent().find(".post_link").attr("href");
                    });
                }
            });
            isLoading = false;
        }
    }

    // initial paosts load
    await loadMorePosts("global");
    await loadMorePosts("following-authors");

    $(window).on('scroll', async function() {
        let active_posts_tab = $("#myTab .posts-tab.active").attr("id");
        if (hasReachedBottom(active_posts_tab)) {
            if (active_posts_tab === "global-posts-tab") {
                await loadMorePosts("global");
            } else {
                await loadMorePosts("following-authors");
            }
        } 
    });
});