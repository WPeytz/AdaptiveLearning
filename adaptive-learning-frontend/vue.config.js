module.exports = {
  devServer: {
    hot: false, // Disable Hot Module Replacement (HMR)
    client: {
      webSocketURL: undefined, // Use undefined instead of false to match schema
    },
  },
};