module.exports = {
    pluginOptions: {
        electronBuilder: {
            nodeIntegration: true,
            externals: ['fsuipc'],
            nodeModulesPath: ['../../node_modules', './node_modules']
        }
    }
}
