const ctx = document.getElementById("myChart");

var labellist = labels.split(",").slice(0, -1);
var data = selectedProductData.split(",").slice(0, -1);
var selectedProductToShow = "";
var translations_char = {
  "%25": "%",
  "%3F": "?",
  "%26": "&",
};

if (selectedProduct.length > 25) {
  selectedProductToShow = selectedProduct.substring(0, 25);
  selectedProductToShow = selectedProductToShow + "...";
} else {
  selectedProductToShow = selectedProduct;
}

function replaceKeysWithValues(inputString) {
  for (var key in translations_char) {
    if (translations_char.hasOwnProperty(key)) {
      var value = translations_char[key];
      var regex = new RegExp(key, "g");
      inputString = inputString.replace(regex, value);
    }
  }

  return inputString;
}

var convertesProductName = replaceKeysWithValues(selectedProduct);

console.log("******selectedProduct , convertedProductName:");
console.log(selectedProduct, convertesProductName);
console.log("***** selectedProductToShow");
console.log(selectedProductToShow);
console.log("***** selectedProductData");
console.log(selectedProductData);
console.log("***** data");
console.log(data);
console.log("***** labels");
console.log(labels);
console.log("***** storeUnit");
console.log(storeUnit);

const options = {
  scales: {
    y: {
      title: {
        display: true,
        text: storeUnit,
      },
    },
  },
  responsive: true,
  plugins: {
    legend: {
      display: false,
      position: "top",
    },
    title: {
      display: true,
      text: convertesProductName,
    },
  },
};

new Chart(ctx, {
  type: "bar",
  data: {
    datasets: [
      {
        label: selectedProductToShow + " in €",
        data: data,
        backgroundColor: "rgb(255, 193, 7)",
      },
    ],
    labels: labellist,
  },
  options: options,
});
