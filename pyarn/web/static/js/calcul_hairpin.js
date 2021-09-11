$("#buttonCalcul").click(function (event) {
    event.preventDefault(); /* prevent form submiting here */

    $(".tmp").remove();
    const button = (this)

    const arn1Value = $("#inputArn1").val();
    const errorMismatchValue = $("#inputPercentPairing").val();

    const messageButton = $("#messageButton");
    messageButton.text("");
    if (arn1Value === "" || errorMismatchValue === 0) {
        messageButton.text("Arn1 or mismatch value are empty");
        return
    }

    button.disabled = true;
    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/calcul/hairpin",
        data: {
            "arn1": arn1Value,
            "percent_pairing": errorMismatchValue,
        },
        dataType: "json",
        success: function (data) {
            $("#textSequenceArn1").text(data["arn1"]);
            $("#textPercentPair").text(data["percent_pair"]);

            console.log(data)

            const htmlToAddInfosCalcul = `
                 <div class="tmp row">
                     <div class="col border border-secondary text-center">
                        <div class="col">
                            <div class="row">
                                <p>%arn1</p>
                            </div>
                            <div class="row">
                                <p>%arn2</p>                         
                            </div>
                        </div>
                     </div>
                     <div class="col border border-secondary text-center">
                        <div class="col">
                            <div class="row">
                                <p>Number Pair %nbPair</p>
                            </div>
                        </div>
                        <div class="col">
                            <div class="row">
                                <p>Percent Pair %percentPair %</p>
                            </div>
                        </div>
                     </div>
                 </div>
             `;

            const divInfosHigherPercentPair = $("#divInfosHigherPercentPair");
            for (let i = 0; i < data["info_percent_pairing"].length; i++) {
                tmp = htmlToAddInfosCalcul.replace("%arn1", data["info_percent_pairing"][i]['sub_arn1']);
                tmp = tmp.replace("%arn2", data["info_percent_pairing"][i]['sub_arn2']);
                tmp = tmp.replace("%nbPair", data["info_percent_pairing"][i]['nb_pair']);
                tmp = tmp.replace("%percentPair", data["info_percent_pairing"][i]['percent_pair']);

                divInfosHigherPercentPair.append(tmp);
            }

            const divToast = $("#liveToast");
            const toast = new bootstrap.Toast(divToast);
            toast.show();

            button.disabled = false;
        },
        error: function (data) {
            button.disabled = false;
            // messageButton.text(data.stringify());
            messageButton.text(data);
        },
    });
});


$("#buttonClear").click(function (event) {
    event.preventDefault(); /* prevent form submiting here */
    const button = (this)
    button.disabled = true;

    $("#inputArn1").val("");

    $("#messageButton").text("");
    $("#textSequenceArn1").val("");

    $("#textPercentPair").text("");

    $(".tmp").remove();

    button.disabled = false;
});