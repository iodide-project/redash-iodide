import React from 'react';
import PropTypes from 'prop-types';
import Button from 'antd/lib/button';
import Icon from 'antd/lib/icon';
import { render } from 'react-dom';

import notification from '@/services/notification';

class IodideButton extends React.Component {
  static propTypes = {
    queryID: PropTypes.string.isRequired,
  };

  constructor(props) {
    super(props);

    this.apiBase = `${window.location.protocol}//${window.location.hostname}${
      window.location.port ? `:${window.location.port}` : ''
    }/api/integrations/iodide`;

    this.spinnerDelay = 250;

    // The ID of the "default" group in the Redash access control system
    this.defaultGroupID = 2;

    this.state = {
      defaultGroupHasAccess: false,
      showSpinner: false,
    };
  }

  componentDidMount() {
    // Iodide does not have an access control system and it certainly does not
    // share access control settings with Redash. When the "Explore in Iodide"
    // button is pressed, the data from that query is made available to all
    // Iodide users.
    //
    // Therefore, we should only show the button if the "default" group in
    // Redash has access to the query.
    fetch(`${this.apiBase}/${this.props.queryID}/groups`)
      .then((response) => {
        if (response.status === 200 && response.headers.get('content-type') === 'application/json') {
          return response.json();
        }
      })
      .then((json) => {
        if (json.groups && json.groups.includes(this.defaultGroupID)) {
          this.setState({ defaultGroupHasAccess: true });
        }
      });
  }

  componentWillUnmount() {
    // Don't attempt to set state after this component unmounts
    clearTimeout(this.spinnerDelayTimeout);
  }

  openIodideNotebook = (queryID) => {
    if (!this.state.defaultGroupHasAccess) return;

    const handleError = (msg = 'Could not create Iodide notebook') => {
      notification.error(msg);
      this.hideSpinner();
      this.iodideWindow.close();
    };

    const handleResponse = (response) => {
      if (response.status === 200 && response.headers.get('content-type') === 'application/json') {
        return response.json();
      }
      handleError('Bad response from Redash server');
    };

    this.showSpinner();

    // Immediately open a window for Iodide. If we open it later, the browser
    // may consider it to be an unwanted popup. We will close it if we encounter
    // an error.
    //
    // https://stackoverflow.com/a/25050893/4297741
    this.iodideWindow = window.open('', '_blank');

    const settingsPromise = fetch(`${this.apiBase}/settings`)
      .then(handleResponse)
      .catch(handleError);

    const notebookPromise = fetch(`${this.apiBase}/${queryID}/notebook`, { method: 'POST' })
      .then(handleResponse)
      .catch(handleError);

    Promise.all([settingsPromise, notebookPromise])
      .then(([{ iodideURL }, { id }]) => {
        this.iodideWindow.location.href = `${iodideURL}notebooks/${id}`;
        this.hideSpinner();
      });
  };

  showSpinner = () => {
    // Only show the spinner if it takes more than this.spinnerDelay
    // milliseconds to open the notebook
    this.spinnerDelayTimeout = setTimeout(() => {
      this.setState({ showSpinner: true });
    }, this.spinnerDelay);
  };

  hideSpinner = () => {
    clearTimeout(this.spinnerDelayTimeout);
    this.setState({ showSpinner: false });
  };

  render() {
    if (!this.state.defaultGroupHasAccess) return null;
    return (
      <Button
        className="explore-in-iodide"
        style={{ marginRight: 5 }}
        onClick={() => this.openIodideNotebook(this.props.queryID)}
      >
        <Icon type={this.state.showSpinner ? 'loading' : 'experiment'} />
        <span className="hidden-xs hidden-s hidden-m">Explore in Iodide</span>
      </Button>
    );
  }
}

export default function init(ngModule) {
  ngModule.decorator('queryControlDropdownDirective', [
    '$delegate',
    ($delegate) => {
      const controller = $delegate[0].controller;
      const controllerFunc = controller[controller.length - 1];
      controllerFunc.prototype.origRender = controllerFunc.prototype.render;

      controllerFunc.prototype.render = function newRender() {
        this.origRender();

        const buttonContainerId = 'explore-in-iodide-container';
        const queryID = window.location.pathname.match(
          /\/queries\/(.*?)(\/|$)/,
        )[1];

        // Don't add the button if it already exists or if the query has never
        // been saved. The button won't work if the query has never been saved.
        if (document.getElementById(buttonContainerId) || queryID === 'new') {
          return;
        }

        const bottomController = document.querySelector('.bottom-controller');
        const queryControlDropdown = bottomController.querySelector(
          'query-control-dropdown',
        );

        const iodideButtonContainer = document.createElement('div');
        iodideButtonContainer.id = buttonContainerId;
        bottomController.insertBefore(
          iodideButtonContainer,
          queryControlDropdown,
        );

        render(<IodideButton queryID={queryID} />, iodideButtonContainer);
      };

      return $delegate;
    },
  ]);
}

init.init = true;
