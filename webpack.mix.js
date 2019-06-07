let mix = require('laravel-mix');

/*
 |--------------------------------------------------------------------------
 | Mix Configuration
 |--------------------------------------------------------------------------
 */

mix.disableNotifications();

let public_path = '';

if (process.env.FLASK_ENV == 'development') {
    mix.sourceMaps(); // Enable sourcemaps
    public_path = 'app/static';
} else {
    public_path = 'public';
}

mix.setPublicPath(public_path);

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 */

mix.sass('app/resources/sass/auth.scss', 'css');

mix.sass('catalog/resources/sass/app.scss', 'css');

mix.copyDirectory('app/resources/images', public_path + '/img');