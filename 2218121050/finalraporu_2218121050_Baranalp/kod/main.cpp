#include <iostream>
#include <fstream>
#include <vector>
#include <opencv2/opencv.hpp>
#include "tensorflow/lite/interpreter.h"
#include "tensorflow/lite/kernels/register.h"
#include "tensorflow/lite/string_util.h"
#include <filesystem>

namespace fs = std::filesystem;

// Function to load labels from a text file
std::vector<std::string> loadLabels(const std::string& labelsFile) {
    std::ifstream file(labelsFile);
    std::vector<std::string> labels;
    std::string line;
    while (std::getline(file, line)) {
        labels.push_back(line);
    }
    return labels;
}

// Resize and preprocess input image to match model input tensor
cv::Mat preprocessInputImage(const cv::Mat& inputImage, int inputWidth, int inputHeight) {
    // Convert input image to grayscale
    cv::Mat grayImage;
    cv::cvtColor(inputImage, grayImage, cv::COLOR_BGR2GRAY);

    // Resize input image to match model input tensor dimensions
    cv::Mat resizedImage;
    cv::resize(grayImage, resizedImage, cv::Size(inputWidth, inputHeight));

    // Convert resized image to float and normalize pixel values
    cv::Mat floatImage;
    resizedImage.convertTo(floatImage, CV_32FC1, 1.0 / 255.0);

    return floatImage;
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <model_file.tflite> <labels_file.txt> <input_folder_path>" << std::endl;
        return 1;
    }

    const char* modelFile = argv[1];
    const char* labelsFile = argv[2];
    const char* inputFolder = argv[3];

    // Load model
    std::unique_ptr<tflite::FlatBufferModel> model = tflite::FlatBufferModel::BuildFromFile(modelFile);
    if (!model) {
        std::cerr << "Failed to load model: " << modelFile << std::endl;
        return 1;
    }

    // Build interpreter
    tflite::ops::builtin::BuiltinOpResolver resolver;
    std::unique_ptr<tflite::Interpreter> interpreter;
    if (tflite::InterpreterBuilder(*model.get(), resolver)(&interpreter) != kTfLiteOk) {
        std::cerr << "Failed to build interpreter" << std::endl;
        return 1;
    }

    // Allocate tensors
    if (interpreter->AllocateTensors() != kTfLiteOk) {
        std::cerr << "Failed to allocate tensors!" << std::endl;
        return 1;
    }

    // Get input tensor details
    int input = interpreter->inputs()[0];
    int inputWidth = interpreter->tensor(input)->dims->data[1];
    int inputHeight = interpreter->tensor(input)->dims->data[2];
    int inputChannels = interpreter->tensor(input)->dims->data[3];

    // Iterate through images in the input folder
    for (const auto& entry : fs::directory_iterator(inputFolder)) {
        std::string imageFile = entry.path().string();
        
        // Load input image using OpenCV
        cv::Mat image = cv::imread(imageFile);
        if (image.empty()) {
            std::cerr << "Failed to read image: " << imageFile << std::endl;
            continue; // Skip to next image
        }

        // Preprocess input image
        cv::Mat inputImage = preprocessInputImage(image, inputWidth, inputHeight);
        

        // Check input tensor dimensions
        if (inputImage.cols != inputWidth || inputImage.rows != inputHeight || inputImage.channels() != inputChannels) {
            std::cerr << "Input image dimensions do not match model input tensor dimensions for: " << imageFile << std::endl;
            continue; // Skip to next image
        }

        // Copy preprocessed input image data to input tensor
        float* inputTensorPtr = interpreter->typed_input_tensor<float>(0);
        if (!inputTensorPtr) {
            std::cerr << "Failed to get input tensor for: " << imageFile << std::endl;
            continue; // Skip to next image
        }
        memcpy(inputTensorPtr, inputImage.data, inputImage.total() * inputImage.elemSize());

        // Run inference
        if (interpreter->Invoke() != kTfLiteOk) {
            std::cerr << "Failed to invoke inference for: " << imageFile << std::endl;
            continue; // Skip to next image
        }

        // Get output tensor details
        int output = interpreter->outputs()[0];
        TfLiteIntArray* outputDims = interpreter->tensor(output)->dims;
        int outputSize = outputDims->data[1];

        // Retrieve output results
        float* outputTensorPtr = interpreter->typed_output_tensor<float>(0);
        if (!outputTensorPtr) {
            std::cerr << "Failed to get output tensor for: " << imageFile << std::endl;
            continue; // Skip to next image
        }

        // Find the label with the highest confidence score
        int maxIndex = -1;
        float maxScore = -1.0f;
        for (int i = 0; i < outputSize; ++i) {
            if (outputTensorPtr[i] > maxScore) {
                maxScore = outputTensorPtr[i];
                maxIndex = i;
            }
        }

        // Load labels
        std::vector<std::string> labels = loadLabels(labelsFile);

        if (maxIndex >= 0 && maxIndex < labels.size()) {
    std::cout << "Image: " << imageFile << "\nLabel: " << labels[maxIndex] << "\nConfidence: " << maxScore << std::endl;

    // Draw confidence value on the image
    std::ostringstream confidenceStr;
    std::ostringstream labeling;
    labeling << "Label: " << labels[maxIndex] ; // Modify this line
    confidenceStr << ", Confidence: " << maxScore; 
    
    // Show image with confidence value
    cv::resize(image, image, cv::Size(512, 512));
    cv::putText(image, labeling.str(), cv::Point(10, 30), cv::FONT_HERSHEY_SIMPLEX, 0.8, cv::Scalar(255, 255, 255), 1);
    cv::putText(image, confidenceStr.str(), cv::Point(10, 60), cv::FONT_HERSHEY_SIMPLEX, 0.8, cv::Scalar(255, 255, 255), 1);
    cv::imshow("Image with Confidence", image);
    
    cv::waitKey(0); // Wait for a key press
} 	else {
    std::cerr << "Failed to retrieve valid label for: " << imageFile << std::endl;
    continue; // Skip to next image
}
    }
	
    return 0;
}
