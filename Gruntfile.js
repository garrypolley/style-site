module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    watch: {
      scripts: {
        files: ['*'],
        tasks: ['less:example'],
        options: {
          spawn: false
        }
      }
    },

    less: {
      example: {
        options: {
          sourceMap: true,
          compress: false,
          sourceMapFilename: 'assets/css/app.css.map'
        },
        files: {
          'assets/css/app.css': 'assets/less/app.less',
        }
      }
    }
  });

  // Load in less
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');

  // Default task(s).
  grunt.registerTask('default', ['less:example', 'watch']);

};
