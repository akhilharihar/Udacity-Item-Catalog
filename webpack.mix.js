let mix = require('laravel-mix');

/*
 |--------------------------------------------------------------------------
 | Mix Configuration
 |--------------------------------------------------------------------------
 */

mix.disableNotifications();

if (process.env.FLASK_ENV == 'development') {
    mix.sourceMaps(); // Enable sourcemaps
    mix.setPublicPath('app/static');
} else {
    mix.setPublicPath('public');
}

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 */

mix.sass('app/resources/sass/auth.scss', 'css');