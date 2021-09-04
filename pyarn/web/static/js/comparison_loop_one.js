$("#buttonCompare").click(function (event) {
    event.preventDefault(); /* prevent form submiting here */

    $(".tmp").remove();
    const button = (this)

    const arn1Value = $("#inputArn1").val();
    const arn2Value = $("#inputArn2").val();
    const errorMismatchValue = $("#inputPercentPairing").val();

    const messageButton = $("#messageButton");
    messageButton.text("");
    if (arn1Value === "" || arn2Value === "" || errorMismatchValue === 0) {
        messageButton.text("Arn1, Arn2 or mismatch value are empty");
        return
    }

    button.disabled = true;
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/compare/loop",
        data: {
            "arn1": arn1Value,
            "arn2": arn2Value,
            "percent_pairing": errorMismatchValue,
        },
        dataType: "json",
        success: function (data) {
            $("#textSequenceArn1").text(data["arn1"]);
            $("#textSequenceArn2").text(data["arn2"]);
            $("#textPercentPair").text(data["percent_pair"]);
            $("#textCanLoop").text(data["can_loop"]);

            console.log(data)

            const htmlToAddInfosComparison = `
                 <div class="tmp row">
                     <div class="col border border-secondary text-center">
                         <p>%s</p>
                     </div>
                 </div>
             `;

            const divInfosHigherPercentPair = $("#divInfosHigherPercentPair");
            if (data["info_pair"]) {
                const divInfosHigherPercentPair = $("#divInfosHigherPercentPair");
                for (let i = 0; i < data["info_pair"].length; i++) {
                    divInfosHigherPercentPair.append(htmlToAddInfosComparison.replace("%s", data["info_pair"][i]));
                }
            } else {
                divInfosHigherPercentPair.append(
                    htmlToAddInfosComparison.replace(
                        "%s",
                        "No infos found because no match with your percent pairing"
                    )
                );
            }

            const divToast = $("#liveToast");
            const toast = new bootstrap.Toast(divToast);
            toast.show();

            button.disabled = false;
        },
        error: function (data) {
            button.disabled = false;
            messageButton.text(data.stringify());
        },
    });
});


$("#buttonClear").click(function (event) {
    event.preventDefault(); /* prevent form submiting here */
    const button = (this)
    button.disabled = true;

    $("#inputArn1").val("");
    $("#inputArn2").val("");

    $("#messageButton").text("");
    $("#textSequenceArn1").val("");
    $("#textSequenceArn2").val("");

    $("#textPercentPair").text("");
    $("#textCanLoop").text("");

    $(".tmp").remove();

    button.disabled = false;
});