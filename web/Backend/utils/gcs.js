const {Storage} = require('@google-cloud/storage');

async function uploadToBucket(bucketName, filePath, file) {
    const storage = new Storage();
    try {
        await storage.bucket(bucketName).file(`${filePath}`).save(file);
    } catch (error) {
        console.log(error);
    }
}

module.exports = {uploadToBucket};