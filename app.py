from flask import Flask, jsonify, request
from flask_cors import CORS
from database import cursor, conn
from controller.ranking_filtering import ranking_filtering
from controller.item_base_filtering import item_base_filtering
from controller.content_base_filtering import content_base_filtering


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "success",
        "message": "Welcome to UMKM Sumbar API Service For Machine Learning" 
    }), 200

    
@app.route('/recomender/item', methods=['GET'])
def item_base_recomender():
    try:
        # Eksekusi query untuk mengambil semua data dari tabel Review Produk
        cursor.execute("SELECT user_id, product_id, rating  FROM product_reviews")
        dataReview = cursor.fetchall()
        # print(dataReview)
        
        # Eksekusi query untuk mengambil semua data dari tabel Produk
        cursor.execute("SELECT products.*, ROUND(COALESCE(AVG(product_reviews.rating), 0), 1) as rating FROM products LEFT JOIN product_reviews ON products.id = product_reviews.product_id GROUP BY products.id")
        dataProduct = cursor.fetchall()
        
        user_id = request.args.get('user_id')
        num_recommendations = request.args.get('num_recommendations')
        num_recommendations = int(num_recommendations) if num_recommendations else 8
        
        if user_id and user_id.isdigit() and user_id in [str(user['user_id']) for user in dataReview]:
            user_id = int(user_id)
            productRecommend = item_base_filtering(dataReview, dataProduct, user_id, num_recommendations)
            
            return jsonify({
                "status": "success",
                "user_id": user_id,
                "filter": "item-based collaborative filtering",
                "recommendations": productRecommend
                }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "user_id not found"
                }), 404
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    
@app.route('/recomender/ranking', methods=['GET'])
def ranking_filtering_recomender():
    try:
        # Eksekusi query untuk mengambil semua data dari tabel Review Produk
        cursor.execute("SELECT user_id, product_id, rating  FROM product_reviews")
        dataReview = cursor.fetchall()
        
        # Eksekusi query untuk mengambil semua data dari tabel Produk
        cursor.execute("SELECT products.*, ROUND(COALESCE(AVG(product_reviews.rating), 0), 1) as rating FROM products LEFT JOIN product_reviews ON products.id = product_reviews.product_id GROUP BY products.id")
        dataProduct = cursor.fetchall()
        
        num_recommendations = request.args.get('num_recommendations')
        num_recommendations = int(num_recommendations) if num_recommendations else 8
        
        productRecommend = ranking_filtering(dataReview=dataReview, dataProduct=dataProduct, num_recommendations=num_recommendations)
        
        return jsonify({
            "status": "success",
            "filter": "popularity ranking filtering",
            "recommendations": productRecommend
            }), 200
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    
@app.route('/recomender/content', methods=['GET'])
def content_based_recomender():
    try:
        cursor.execute("SELECT products.*, ROUND(COALESCE(AVG(product_reviews.rating), 0), 1) as rating, COUNT(product_reviews.rating) as rating_count FROM products LEFT JOIN product_reviews ON products.id = product_reviews.product_id GROUP BY products.id")
        dataProduct = cursor.fetchall()
        
        product_id = request.args.get('product_id')
        num_recommendations = request.args.get('num_recommendations')
        num_recommendations = int(num_recommendations) if num_recommendations else 8
        
        if product_id and product_id.isdigit() and product_id in [str(product['id']) for product in dataProduct]:
            product_id = int(product_id)
            productRecommend =  content_base_filtering(product_id=product_id, dataProduct=dataProduct, num_recommendations=num_recommendations)
            return jsonify({
                "status": "success",
                "filter": "content-based filtering",
                "recommendations": productRecommend
                }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "product_id not found"
                }), 404
            
    except Exception as err:
        return jsonify({'error': str(err)}), 500
    
@app.route('/chatbot', methods=['POST'])
def chatbot_nlp():
    return jsonify({
        "status": "success",
        "message": "Chatbot NLP"
    }), 200
        

if __name__ == '__main__':
    app.run(debug=True)