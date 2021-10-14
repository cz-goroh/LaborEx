'use strict';

let project_folder = 'dist',
  source_folder = 'src';

let fs = require('fs');

let path = {
  build: {
    html: project_folder + '/',
    css: project_folder + '/css/vendor/',
    scss: project_folder + '/css/',
    js: project_folder + '/js/',
    jsLibs: project_folder + '/js/libs/',
    img: project_folder + '/img/',
    video: project_folder + '/video/',
    fonts: project_folder + '/fonts/',
  },
  src: {
    html: [source_folder + '/*.html', '!' + source_folder + '/_*.html'],
    css: source_folder + '/scss/vendor/*.css',
    scss: [source_folder + '/scss/style.scss', '!' + source_folder + '/scss/**/_*.scss'],
    js: [source_folder + '/js/**/*.js', '!' + source_folder + '/js/libs/*.js'],
    jsLibs: source_folder + '/js/libs/*.js',
    img: source_folder + '/img/**/*.{jpg,png,gif,ico,webp,svg}',
    video: source_folder + '/video/*.*',
    fonts: source_folder + '/fonts/*.ttf',
  },
  watch: {
    html: source_folder + '/**/*.html',
    css: source_folder + '/scss/vendor/*.css',
    scss: source_folder + '/scss/**/*.scss',
    js: source_folder + '/js/**/*.js',
    jsLibs: source_folder + '/js/libs/*.js',
    img: source_folder + '/img/**/*.{jpg,png,svg,gif,ico,webp}',
  },
  clean: './' + project_folder + '/',
};

let { src, dest } = require('gulp'),
  gulp = require('gulp'),
  browsersync = require('browser-sync').create(),
  del = require('del'),
  fileinclude = require('gulp-file-include'),
  sass = require('gulp-sass')(require('sass')),
  notify = require('gulp-notify'),
  autoprefixer = require('gulp-autoprefixer'),
  sourcemaps = require('gulp-sourcemaps'),
  cleanCSS = require('gulp-clean-css'),
  rename = require('gulp-rename'),
  uglify = require('gulp-uglify-es').default,
  imagemin = require('gulp-imagemin'),
  webp = require('gulp-webp'),
  webphtml = require('gulp-webp-html'),
  svgSprite = require('gulp-svg-sprite'),
  ttf2woff = require('gulp-ttf2woff'),
  ttf2woff2 = require('gulp-ttf2woff2'),
  fonter = require('gulp-fonter');

function browserSync(params) {
  browsersync.init({
    server: {
      baseDir: './' + project_folder + '/',
    },
    port: 3000,
    browser: 'chrome',
  });
}

function html(params) {
  return src(path.src.html).pipe(fileinclude()).pipe(dest(path.build.html)).pipe(browsersync.stream());
}

const css = () => {
  return src(path.src.css).pipe(dest(path.build.css)).pipe(browsersync.stream());
};

const scss = () => {
  return src('./src/scss/**/*.scss')
    .pipe(sourcemaps.init())
    .pipe(
      sass({
        outputStyle: 'expanded',
      }).on('error', notify.onError())
    )
    .pipe(
      autoprefixer({
        cascade: false,
      })
    )
    .pipe(dest('./dist/css/'))
    .pipe(
      rename({
        suffix: '.min',
      })
    )
    .pipe(
      cleanCSS({
        level: 2,
      })
    )
    .pipe(sourcemaps.write('.'))
    .pipe(dest('./dist/css/'))
    .pipe(browsersync.stream());
};

function js(params) {
  return (
    src(path.src.js)
      // .pipe(fileinclude())
      .pipe(dest(path.build.js))
      .pipe(uglify())
      .pipe(
        rename({
          extname: '.min.js',
        })
      )
      .pipe(dest(path.build.js))
      .pipe(browsersync.stream())
  );
}

function jsLibs(params) {
  return src(path.src.jsLibs).pipe(dest(path.build.jsLibs));
}

function images(params) {
  return (
    src(path.src.img)
      // .pipe(
      //   webp({
      //     quality: 70,
      //   })
      // )
      .pipe(dest(path.build.img))
      .pipe(src(path.src.img))
      .pipe(
        imagemin({
          progressive: true,
          svgoPlugins: [{ removeViewBox: false }],
          interlaced: true,
          optimizationLevel: 3, // 0 to 7
        })
      )
      .pipe(dest(path.build.img))
      .pipe(browsersync.stream())
  );
}

function video(params) {
  return src(path.src.video).pipe(dest(path.build.video));
}

function fonts(params) {
  src(path.src.fonts).pipe(ttf2woff()).pipe(dest(path.build.fonts));
  return src(path.src.fonts).pipe(ttf2woff2()).pipe(dest(path.build.fonts));
}

gulp.task('otf2ttf', function () {
  return src([source_folder + '/fonts/*.otf'])
    .pipe(
      fonter({
        formats: ['ttf'],
      })
    )
    .pipe(dest(source_folder + '/fonts/'));
});

const svgSprites = () => {
  return src('./src/img/icons/**.svg')
    .pipe(
      svgSprite({
        mode: {
          stack: {
            sprite: '../icons/sprite.svg',
          },
        },
      })
    )
    .pipe(dest('./dist/img/'));
};

function fontsStyle(params) {
  let file_content = fs.readFileSync(source_folder + '/scss/_fonts.scss');
  if (file_content == '') {
    fs.writeFile(source_folder + '/scss/_fonts.scss', '', cb);
    return fs.readdir(path.build.fonts, function (err, items) {
      if (items) {
        let c_fontname;
        for (var i = 0; i < items.length; i++) {
          let fontname = items[i].split('.');
          fontname = fontname[0];
          if (c_fontname != fontname) {
            fs.appendFile(
              source_folder + '/scss/_fonts.scss',
              '@include font("' + fontname + '", "' + fontname + '", "400", "normal");\r\n',
              cb
            );
          }
          c_fontname = fontname;
        }
      }
    });
  }
}

function cb() {}

function watchFiles(params) {
  gulp.watch([path.watch.html], html);
  gulp.watch([path.watch.css], css);
  gulp.watch([path.watch.scss], scss);
  gulp.watch([path.watch.js], js);
  gulp.watch([path.watch.jsLibs], jsLibs);
  gulp.watch([path.watch.img], images);
  gulp.watch('./src/img/icons/*.svg', svgSprites);
}

function clean(params) {
  return del(path.clean);
}

let build = gulp.series(
  clean,
  gulp.parallel(js, jsLibs, css, scss, html, images, fonts, svgSprites, video),
  fontsStyle
);
let watch = gulp.parallel(build, watchFiles, browserSync);

exports.fontsStyle = fontsStyle;
exports.fonts = fonts;
exports.video = video;
exports.images = images;
exports.svgSprites = svgSprites;
exports.js = js;
exports.jsLibs = jsLibs;
exports.css = css;
exports.scss = scss;
exports.html = html;
exports.build = build;
exports.watch = watch;
exports.default = watch;
