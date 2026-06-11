{{
    config(
        materialized='table'
    )
}}

{{ read_zipcode_csv(
    'zip://https://www.post.japanpost.jp/service/search/zipcode/download/utf/zip/utf_ken_all.zip/utf_ken_all.csv'
) }}
