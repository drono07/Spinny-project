# Basic API service for Box CRUD Operations

## 1. Get Authentication Token API - using username and password

<pre><code>
--Request Method POST 'http://127.0.0.1:8000/bozes/api/login' 
--data-raw '{
    "username":"dhruv",
    "password":"dhruv"
}'
--Response : Token Generated 234801022f6bb26fb2f4b424b37555bc5213c571
</code></pre>

## 2. Box Creation API

<pre><code>
--Request Method POST 'http://127.0.0.1:8000/boxes/create/' 
--header 'Authorization: Token 234801022f6bb26fb2f4b424b37555bc5213c571 ' 
--data-raw in Body'{
    "length":6,
    "breadth":9,
    "height":5
}'
-- Responsse : 
----{
    "id": 41,
    "length": 6,
    "breadth": 9,
    "height": 5,
    "area": 258,
    "volume": 270,
    "created_at": "2022-09-29T16:53:13.223918Z",
    "updated_at": "2022-09-29T16:53:13.223918Z",
    "created_by": "dhruv"
}

</code></pre>

## 3. Box Listing API using Various filter

<pre><code>
--Request Method GET 'http://127.0.0.1:8000/boxes/list/' 
--header 'Authorization: Token 234801022f6bb26fb2f4b424b37555bc5213c571 '
--Response :    {
        "id": 41,
        "length": 6,
        "breadth": 9,
        "height": 5,
        "area": 258,
        "volume": 270,
        "created_at": "2022-09-29T16:53:13.223918Z",
        "updated_at": "2022-09-29T16:53:13.223918Z",
        "created_by": "dhruv"
    }
</code></pre>

## Filters 
<pre><code>
1. length__lt
2. length__gt
3. width__lt
4. width__gt
5. height__lt
6. height__gt
7. created_by
</code></pre>

## 4. Box Listing for specific user .
<pre><code>
--Reques Method: GET 'http://127.0.0.1:8000/boxes/list/my_boxes/?length__lt=100 & area__gt=100 & volume__lt = 100 & created_by=dhruv' 
--header 'Authorization: Token 234801022f6bb26fb2f4b424b37555bc5213c571 '
--Response : {
        "id": 41,
        "length": 6,
        "breadth": 9,
        "height": 5,
        "area": 258,
        "volume": 270,
        "created_at": "2022-09-29T16:53:13.223918Z",
        "updated_at": "2022-09-29T16:53:13.223918Z",
        "cr
</code></pre>

Filters 
1.length__lt
2.length__gt
3.width__lt
4.width__gt
5.height__lt
6.height__gt

## 4. Box Deletion API

<pre><code>
--Request Method: DELETE 'http://127.0.0.1:8000/boxes/delete/5' 
--header 'Authorization: Token 234801022f6bb26fb2f4b424b37555bc5213c571 '
--Request : Box Deleted
</code></pre>


## 5. Box Updation API

<pre><code>
Request Method 'http://127.0.0.1:8000/store/box/update/7' 
--header 'Authorization: Token 234801022f6bb26fb2f4b424b37555bc5213c571 ' 
--data-form-data '{
    "length":10,
    "width":3,
    "height":1
}'
--Response: Successfully Updated
</code></pre>


