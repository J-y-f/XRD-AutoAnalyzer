from autoXRD.multiphase_tools import *


def analyze(spectrum_dir, reference_dir):
    """
    Perform phase identification foor a given set of XRD spectra

    Args:
        spectrum_dir: path to directory containing spectra to be classified.
            Note these files should be in xy format.
        reference_dir: path to directory containing CIFs of reference phases
    Returns:
        spectrum_names: filenames of spectra being classified
        predicted_phases: a list of the predicted phases in the mixture
        confidences: the associated confidence with the prediction above
    """

    reference_phases = sorted(os.listdir(reference_dir))
    model = tf.keras.models.load_model('Model.h5', custom_objects={'sigmoid_cross_entropy_with_logits_v2': tf.nn.sigmoid_cross_entropy_with_logits})
    kdp = KerasDropoutPrediction(model)

    spectrum_names, predicted_phases, confidences = [], [], []
    for fname in os.listdir(spectrum_dir):
        total_confidence, all_predictions = [], []
        tabulate_conf, predicted_cmpd_set = [], []
        mixtures, confidence = classify_mixture('%s/%s' % (spectrum_dir, fname), kdp, reference_phases)
        if len(confidence) > 0:
            max_conf_ind = np.argmax(confidence)
            max_conf = 100*confidence[max_conf_ind]
            predicted_cmpds = [fname[:-4] for fname in mixtures[max_conf_ind]]
            predicted_set = ' + '.join(predicted_cmpds)
        else:
            max_conf = 0.0
            predicted_set = 'None'
        spectrum_names.append(fname)
        predicted_phases.append(predicted_set)
        confidences.append(max_conf)

    return spectrum_names, predicted_phases, confidences
