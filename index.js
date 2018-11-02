console.log('Loading Lambda HTML');

exports.handler = function(event, context) {
    var html = '<html><head><title>Hello World From Lambda</title></head>' +
        '<body><h1>Hello World from the pipeline!</h1></body></html>';

    context.succeed(html);
};
