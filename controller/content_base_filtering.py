import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def content_base_filtering(product_id, dataProduct, num_recommendations):
    # Memuat data dari file CSV
    products_df = pd.DataFrame(dataProduct)

    # Menggabungkan tag menjadi satu string per baris
    products_df['tags'] = products_df['tags'].str.replace(',', ' ')

    # Membuat TF-IDF Vectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Mengubah teks tag menjadi matriks TF-IDF
    tfidf_matrix = tfidf_vectorizer.fit_transform(products_df['tags'])

    # Menghitung kesamaan cosine antara semua produk
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Fungsi untuk mendapatkan rekomendasi produk berdasarkan produk yang diberikan
    def get_recommendations(product_id, cosine_sim=cosine_sim):
        # Mendapatkan indeks produk yang sesuai dengan product_id
        idx = products_df[products_df['id'] == product_id].index[0]

        # Mendapatkan skor kesamaan produk yang diberikan dengan semua produk lainnya
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Mengurutkan produk berdasarkan skor kesamaan
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Mendapatkan indeks produk dari 10 produk yang paling mirip
        sim_scores = sim_scores[1:num_recommendations + 1]
        product_indices = [i[0] for i in sim_scores]

        # Mengembalikan ID dari 10 produk yang paling mirip
        return products_df['id'].iloc[product_indices].tolist()

    # Contoh mendapatkan rekomendasi produk yang mirip dengan produk dengan product_id 10
    recommendations = get_recommendations(product_id)
    productRecommend = []
    for item in recommendations:
        product = {'product_id': item, 'product': list(filter(lambda x: x['id'] == item, dataProduct))}
        productRecommend.append(product)
    
    return productRecommend
