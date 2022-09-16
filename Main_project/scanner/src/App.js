import React, {Component} from "react";
import BarcodeScannerComponent from "react-webcam-barcode-scanner";

// import "./Scanner.css";

class Scanner extends Component {
    state = {
        codeList: {},
        isDone: false,
        isScanned: false,
        goodData: {}
    };

    addBarCodeHandler = (code) => {
        if (!this.state.isScanned) {
            console.log()
            console.log(code);
            this.setState((state) => {
                return {
                    codeList: code,
                    isScanned: true
                };
            });
        }
    };

    clearRecordsHandler = () => {
        this.setState({
            codeList: {},
            isScanned: false,
            isDone: true,
            goodData: {}
        });

    };

    doneBtnHandler = () => {
        this.sendPOSTcode(this.state.codeList)
        this.setState((state) => {
            return {
                isDone: false
            };
        });
    };

    sendPOSTcode = (list) => {
        fetch('/codes', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                codelist: list
            })
        }).then(response => {
            if (response.status === 200) {
                console.log("SUCCESSS")
                return response.json();
            }
        }).then(data => {
            this.setState((state) => {
            return {
                goodData: data
            };
        });
            console.log(data);
        })
    }

    showCode = () => {
        let item = this.state.codeList.text;
        return (<p key={item}>{item}</p>);
    }

    classes = [];

    render() {
        if (this.state.isDone) {
            this.classes = ["cameraOutput", "hideVideo"];
        } else {
            this.classes = ["cameraOutput"];
        }
        return (
            <div className="App">
                <div className={this.classes.join("")}>
                    {(
                        <BarcodeScannerComponent
                            width={400}
                            height={400}
                            onUpdate={(err, result) => {
                                if (result) {
                                    // console.log(result);
                                    this.addBarCodeHandler(result);
                                }
                            }}
                        />
                    )}
                </div>
                <div className="resultList">
                    {
                        this.showCode()
                    }
                </div>
                <div className="goodList">
                    <pre>{JSON.stringify(this.state.goodData, null, 2) }</pre>
                </div>
                <div className="bottomControls">
                    <button onClick={this.clearRecordsHandler}>CLEAR</button>
                    <button onClick={this.doneBtnHandler}>DONE</button>
                </div>
            </div>
        );
    }
}

export default Scanner;
