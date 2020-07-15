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

# Everything combined
`input/todo.html` should contain product links.
`input/music.mp3` music to be used in the video

The script will automatically parse links from `input/todo.html` and download their images alongside their metadata such as price and brand.
Then the script will make a product video with the generated pictures and the provided music track:
```shell script
./do_all.sh
```

## Video example

Video example can be found at `examples/example_vid.mov`
