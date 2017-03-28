/**
 * Copyright 2016, GeoSolutions Sas.
 * All rights reserved.
 *
 * This source code is licensed under the BSD-style license found in the
 * LICENSE file in the root directory of this source tree.
 */

/*  DESCRIPTION
    This component contain an input field for holding the url and an icon to
    copy to the clipbard the relatie url.
*/

// components required
const React = require('react');
const CopyToClipboard = require('react-copy-to-clipboard');
const Message = require('../../MapStore2/web/client/components/I18N/Message');
const {Glyphicon, Tooltip, OverlayTrigger, Button} = require('react-bootstrap');

const ShareLink = React.createClass({
    propTypes: {
        shareUrl: React.PropTypes.string
    },
    getInitialState() {
        return {copied: false};
    },
    render() {
        const tooltip = (<Tooltip className="in" placement="bottom" id="tooltip-share" style={{zIndex: 2001}}>
          {this.state.copied ? <Message msgId="share.msgCopiedUrl"/> : <Message msgId="share.msgToCopyUrl"/>}
      </Tooltip>);
        return (<OverlayTrigger placement="bottom" overlay={tooltip}>
                            <CopyToClipboard text={this.props.shareUrl} onCopy={ () => this.setState({copied: true}) } >
                                <Button bsStyle="primary" onMouseLeave={() => {this.setState({copied: false}); }} >
                                    <Glyphicon glyph="copy"/>
                                </Button>
                            </CopyToClipboard>
                        </OverlayTrigger>);
    }
});

module.exports = ShareLink;
