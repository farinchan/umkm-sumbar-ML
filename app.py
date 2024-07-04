from flask import Flask, jsonify, request
import mysql.connector
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Konfigurasi database
db_config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'umkm_sumbar'
}

# Rute API untuk mengambil data dari tabel users
@app.route('/recomender', methods=['GET'])
def recomender_system():
    try:
        # Koneksi ke database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Eksekusi query untuk mengambil semua data dari tabel Review Produk
        cursor.execute("SELECT user_id, product_id, rating  FROM product_reviews")
        dataReview = cursor.fetchall()
        
        # Eksekusi query untuk mengambil semua data dari tabel Produk
        cursor.execute("SELECT products.*, ROUND(COALESCE(AVG(product_reviews.rating), 0), 1) as rating FROM products LEFT JOIN product_reviews ON products.id = product_reviews.product_id GROUP BY products.id")
        dataProduct = cursor.fetchall()
        
        # Tutup koneksi
        cursor.close()
        conn.close()
        
        user_id = request.args.get('user_id')
        num_recommendations = request.args.get('num_recommendations')
        num_recommendations = int(num_recommendations) if num_recommendations else 8
        
        if user_id and user_id.isdigit() and user_id in [str(user['user_id']) for user in dataReview]:
            
            user_id = int(user_id)
            df = pd.DataFrame(dataReview)
            print(df)
            
            # Membuat matriks pivot untuk rating
            utility_matrix = df.pivot_table(values='rating', index='user_id', columns='product_id', fill_value=0)
            print(utility_matrix)
            
            # Menghitung cosine similarity antar item
            item_similarity = cosine_similarity(utility_matrix.T)
            item_similarity_df = pd.DataFrame(item_similarity, index=utility_matrix.columns, columns=utility_matrix.columns)
            print(item_similarity_df)
            
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
            
            # Contoh mendapatkan rekomendasi untuk user_id=1
            recommendations = get_item_recommendations(user_id, utility_matrix, item_similarity_df)
            productRecommend = []
            for item, score in recommendations:
                product = {'product_id': item, 'score': score, 'product': dataProduct[item-1]}
                productRecommend.append(product)
            
            return jsonify({
                "status": "success",
                "user_id": user_id,
                "filter": "item-based collaborative filtering",
                "recommendations": productRecommend
                }), 200
        else:
            df = pd.DataFrame(dataReview)
            
            average_ratings = df.groupby('product_id')['rating'].mean().reset_index(name='average_rating')
            rating_counts = df.groupby('product_id').size().reset_index(name='rating_count')
            ratings_summary = pd.merge(average_ratings, rating_counts, on='product_id')
            print(ratings_summary)

            
            def get_top_rated_recommendations(sorted_ratings, num_recommendations=num_recommendations):
                sorted_ratings = ratings_summary.sort_values(by=['average_rating', 'rating_count'], ascending=False)
                top_rated_items = sorted_ratings.head(num_recommendations)

                return top_rated_items

            # Contoh mendapatkan rekomendasi item terpopuler
            recommendations = get_top_rated_recommendations(ratings_summary).to_dict(orient='records')
            productRecommend = []
            for item in recommendations:
                product = {'product_id': item['product_id'], 'average_rating': item['average_rating'], 'rating_count': item['rating_count'], 'product': dataProduct[item['product_id']-1]}
                productRecommend.append(product)
            
            return jsonify({
                "status": "success",
                "user_id": None,
                "filter": "popularity ranking filtering",
                "recommendations": productRecommend
                }), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    
@app.route('/chatbot', methods=['POST'])

def chatbot_nlp():
    return jsonify({
        "status": "success",
        "message": "Chatbot NLP"
    }), 200
        

if __name__ == '__main__':
    app.run(debug=True)