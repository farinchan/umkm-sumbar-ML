import pandas as pd

def ranking_filtering(dataReview, dataProduct, num_recommendations):
    df = pd.DataFrame(dataReview)
    
    average_ratings = df.groupby('product_id')['rating'].mean().reset_index(name='average_rating')
    rating_counts = df.groupby('product_id').size().reset_index(name='rating_count')
    ratings_summary = pd.merge(average_ratings, rating_counts, on='product_id')

    
    def get_top_rated_recommendations(sorted_ratings, num_recommendations=num_recommendations):
        sorted_ratings = ratings_summary.sort_values(by=['average_rating', 'rating_count'], ascending=False)
        top_rated_items = sorted_ratings.head(num_recommendations)

        return top_rated_items

    recommendations = get_top_rated_recommendations(ratings_summary).to_dict(orient='records')
    productRecommend = []
    for item in recommendations:
        # product = {'product_id': item['product_id'], 'average_rating': item['average_rating'], 'rating_count': item['rating_count'], 'product': dataProduct[item['product_id']-1]}
        productRecommend.append(item['product_id'])
    
    return productRecommend