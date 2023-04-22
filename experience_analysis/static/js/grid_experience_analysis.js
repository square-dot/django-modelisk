function openGrid() {
    const data = new Array(40) // number of rows
        .fill()
        .map((_, row) =>
            new Array(20) // number of columns
                .fill()
                .map((_, column) => ``)
        );

    const container = document.querySelector("#input_grid");
    const hot = new Handsontable(container, {
        data: data,
        rowHeaders: true,
        colHeaders: true,
        height: "auto",
        licenseKey: "non-commercial-and-evaluation", // for non-commercial use only
    });
}
