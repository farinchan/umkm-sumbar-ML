
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def item_base_filtering(dataReview, dataProduct , user_id, num_recommendations):
    df = pd.DataFrame(dataReview)
    utility_matrix = df.pivot(index='user_id', columns='product_id', values='rating').fillna(0)
    
    item_similarity = cosine_similarity(utility_matrix.T)
    item_similarity_df = pd.DataFrame(item_similarity, index=utility_matrix.columns, columns=utility_matrix.columns)
    
    def get_item_recommendations(user_id, utility_matrix, item_similarity_df, num_recommendations=num_recommendations):
        user_ratings = utility_matrix.loc[user_id]
        rated_items = user_ratings[user_ratings > 0].index.tolist()
        
        scores = {}
        for item in rated_items:
            similar_items = item_similarity_df[item].sort_values(ascending=False).index.tolist()
            for similar_item in similar_items:
                if similar_item not in rated_items:
                    if similar_item not in scores:
                        scores[similar_item] = item_similarity_df[item][similar_item] * user_ratings[item]
                    else:
                        scores[similar_item] += item_similarity_df[item][similar_item] * user_ratings[item]

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        recommendations = sorted_scores[:num_recommendations]
        return recommendations
    
    recommendations = get_item_recommendations(user_id, utility_matrix, item_similarity_df)
    productRecommend = []
    for item, score in recommendations:
        product = {'product_id': item, 'score': score, 'product': dataProduct[item-1]}
        productRecommend.append(product)
    
    return productRecommend