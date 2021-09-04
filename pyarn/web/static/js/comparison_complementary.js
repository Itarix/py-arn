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

    const spaceSequence1 = $("#flexRadioAddSpaceArn1");
    const addSpaceSequence1 = spaceSequence1.is(':checked');
    button.disabled = true;
    console.log(addSpaceSequence1)
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/compare/complementary",
        data: {
            "arn1": arn1Value,
            "arn2": arn2Value,
            "percent_pairing": errorMismatchValue,
            "add_space_sequence_1": addSpaceSequence1
        },
        dataType: "json",
        success: function (data) {
            $("#textSequenceArn1").text(data["arn1"]);
            $("#textSequenceArn2").text(data["arn2"]);
            $("#textPercentPair").text(data["percent_pair"]);

            console.log(data)
            $("#textAddSpaceSequence1").text(data["add_space_sequence_1"]);
            $("#textAddSpaceSequence2").text(data["add_space_sequence_2"]);

            const htmlToAddInfosComparison = `
                 <div class="tmp row">
                     <div class="col border border-secondary text-center">
                         <p>%s</p>
                     </div>
                 </div>
             `;

            const divInfosCanPair = $("#divInfosCanPair");
            for (let i = 0; i < data["info_can_pair"].length; i++) {
                divInfosCanPair.append(htmlToAddInfosComparison.replace("%s", data["info_can_pair"][i]));
            }

            const divInfosHigherPercentPair = $("#divInfosHigherPercentPair");
            for (let i = 0; i < data["info_percent_pairing"].length; i++) {
                divInfosHigherPercentPair.append(htmlToAddInfosComparison.replace("%s", data["info_percent_pairing"][i]));
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
    $("#textAddSpaceSequence1").text("");
    $("#textAddSpaceSequence2").text("");

    $(".tmp").remove();

    button.disabled = false;
});