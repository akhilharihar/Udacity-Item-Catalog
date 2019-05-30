let mix = require('laravel-mix');

/*
 |--------------------------------------------------------------------------
 | Mix Configuration
 |--------------------------------------------------------------------------
 */

mix.disableNotifications();
mix.setPublicPath('public');

if (process.env.FLASK_ENV == 'development') {
    mix.sourceMaps(); // Enable sourcemaps
}

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 */