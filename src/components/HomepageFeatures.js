import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

// Import images
import EmbodiedIntelligenceImg from '@site/static/img/physical-ai.jpg';
import ControlSystemsImg from '@site/static/img/robot02.jpg';
import HumanCenteredDesignImg from '@site/static/img/humanoid-robot03.jpg';

const FeatureList = [
  {
    title: 'Embodied Intelligence',
    image: EmbodiedIntelligenceImg,
    description: (
      <p>
        Learn how physical embodiment shapes intelligent behavior through
        sensorimotor dynamics and real-world interaction.
      </p>
    ),
  },
  {
    title: 'Advanced Control Systems',
    image: ControlSystemsImg,
    description: (
      <p>
        Master sophisticated control algorithms for dynamic balance,
        locomotion, and manipulation in humanoid robots.
      </p>
    ),
  },
  {
    title: 'Human-Centered Design',
    image: HumanCenteredDesignImg,
    description: (
      <p>
        Understand principles of human-robot interaction and
        socially intelligent robotics.
      </p>
    ),
  },
];

function Feature({ image, title, description }) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img
          src={image}
          alt={title}
          className={styles.featureImage}
        />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}