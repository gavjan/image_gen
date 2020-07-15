# Generate product photos from product page

```shell script
./run.sh <product_link>
```
example:
```shell script
./run.sh "https://topsale.am/product/adidas-must-haves-emblem-tee/14810/"
```

## Examples generated
<p align="center">
  <img src="examples/standard/846e6ff61e4a9a558f7eMust_Haves_Emblem_Tee_White_ED7272_21_model.png" height="350" width="350" title="Click to Open">
  <img src="examples/standard/bf8662ce483d96871fb4Untitled-1.png" height="350" width="350" title="Click to Open">
  <img src="examples/standard/106368865_2384585271841445_6638484179430715958_n.png" height="350" width="350" title="Click to Open">
</p>

## Split Images Examples generated
<p align="center">
  <img src="examples/split_image/9b9f3dbc4006e8350a9cUntitled-1.png" height="350" width="350" title="Click to Open">
  <img src="examples/split_image/89b68cf09b3851fbc731jdsijs.png" height="350" width="350" title="Click to Open">
  <img src="examples/split_image/3385f05229575dbad629asjkhdhsa.png" height="350" width="350" title="Click to Open">
  <img src="examples/split_image/c464fd10360ada381b76hjvhjvghj.png" height="350" width="350" title="Click to Open">
</p>

# Everything combined
`todo.html` should contain product links.

The script will automatically parse links from `todo.html` and download their images alongside their metadata such as price and brand.
Then the script will generate a product video with pictures from directory `results`, end-screen logo `assets/end_logo.png` and with music from `music/music.mp3`:
```shell script
./do_all.sh
```

## Video example

Video example can be found at `examples/example_vid.mp4`
