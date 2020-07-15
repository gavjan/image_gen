# Generate product photos/videos from Topsale.am product page

To generate a product image
```shell script
./run.sh <product_link>
```
example:
```shell script
./run.sh "https://topsale.am/product/adidas-03-qt-t-shirt-ladies-white/15201/"
```

## Examples generated
<p align="center">
  <img src="examples/standard/9b9f3dbc4006e8350a9cUntitled-1.png" height="350" width="350" title="Click to Open">
  <img src="examples/standard/8008bccdeefcfb7e8571tommmmmmmmmmmmmmm.png" height="350" width="350" title="Click to Open">
  <img src="examples/standard/b66c77c454bef8cb323baaa.png" height="350" width="350" title="Click to Open">
</p>

## Split Images Examples generated
<p align="center">
  <img src="examples/split_image/9b9f3dbc4006e8350a9cUntitled-1.png" height="350" width="350" title="Click to Open">
  <img src="examples/split_image/89b68cf09b3851fbc731jdsijs.png" height="350" width="350" title="Click to Open">
  <img src="examples/split_image/c464fd10360ada381b76hjvhjvghj.png" height="350" width="350" title="Click to Open">
</p>

# Everything combined
`input/todo.html` should contain product links.

The script will automatically parse links from `input/todo.html` and download their images alongside their metadata such as price and brand.
Then the script will generate a product video with pictures from directory `results`, end-screen logo `assets/end_logo.png` and with music from `input/music.mp3`:
```shell script
./do_all.sh
```

## Video example

Video example can be found at `examples/example_vid.mov`
